import copy
import os

import torch
from matplotlib import pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay, classification_report


def make_save_dirs(root_dir):
    img_dir = os.path.join(root_dir, 'images')
    model_dir = os.path.join(root_dir, 'checkpoints')
    os.makedirs(img_dir, exist_ok=True)
    os.makedirs(model_dir, exist_ok=True)
    print(f'The output folder:{img_dir},{model_dir} has been created.')
    return img_dir, model_dir


def calculate_metric(all_labels, all_predictions, classes, class_metric=False, average='macro avg'):
    metric = classification_report(y_true=all_labels, y_pred=all_predictions, target_names=classes
                                   , digits=4, output_dict=True)
    if not class_metric:
        metric = {
            'accuracy': metric.get('accuracy'),
            'precision': metric.get(average).get('precision'),
            'recall': metric.get(average).get('recall'),
            'f1-score': metric.get(average).get('f1-score'),
        }
        return metric
    else:
        return metric


def plot_confusion_matrix(all_labels,
                          all_predictions,
                          classes,
                          name='confusion_matrix.png',
                          normalize=None,
                          cmap=plt.cm.Blues,
                          ):
    ConfusionMatrixDisplay.from_predictions(all_labels,
                                            all_predictions,
                                            display_labels=classes,
                                            cmap=cmap,
                                            normalize=normalize,
                                            xticks_rotation=45
                                            )
    plt.savefig(name, dpi=500)
    plt.close()


def auto_batch_size(
    model,
    criterion,
    optimizer,
    dataset_sample,
    device,
    max_possible=1024,
    memory_ratio=1.0
):
    """
    Automatically find the maximum feasible batch size based on GPU memory.

    Args:
        model:
        criterion:
        optimizer:
        dataset_sample:  (input_sample, label_sample)
        device:
        max_possible:
        memory_ratio:

    Returns:
    """
    model.to(device)
    if not (0 < memory_ratio <= 1):
        raise ValueError("memory_ratio must be between 0 and 1.")
    total_memory = torch.cuda.get_device_properties(device).total_memory
    allowed_memory = total_memory * memory_ratio
    print(f"Total GPU Memory: {total_memory / 1024**3:.2f} GB")
    print(f"Allowed Memory ({memory_ratio*100}%): {allowed_memory / 1024**3:.2f} GB")

    model.train()
    input_sample, label_sample = dataset_sample
    input_sample = input_sample.to(device)
    label_sample = label_sample.to(device)

    model_init = copy.deepcopy(model.state_dict())
    optimizer_init = copy.deepcopy(optimizer.state_dict())

    def try_batch_size(batch_size):

        model.load_state_dict(model_init)
        optimizer.load_state_dict(optimizer_init)
        torch.cuda.empty_cache()
        torch.cuda.reset_peak_memory_stats(device)

        try:
            inputs = input_sample.unsqueeze(0).expand(batch_size, *input_sample.shape).contiguous()
            labels = label_sample.unsqueeze(0).expand(batch_size, *label_sample.shape).contiguous()
        except RuntimeError as e:
            print(f"Error generating batch size {batch_size}: {e}")
            return False

        try:
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            peak_memory = torch.cuda.max_memory_allocated(device)
            if peak_memory > allowed_memory:
                print(f"Batch size {batch_size} exceeds allowed memory: {peak_memory / 1024**3:.2f} GB > {allowed_memory / 1024**3:.2f} GB")
                return False

            del inputs, outputs, loss
            torch.cuda.empty_cache()
            return True

        except RuntimeError as e:
            if 'CUDA out of memory' in str(e):
                del inputs, labels
                torch.cuda.empty_cache()
                return False
            else:
                raise e

    batch_size = 1
    while batch_size <= max_possible:
        if try_batch_size(batch_size):
            batch_size *= 2
        else:
            break

    if batch_size == 1 and not try_batch_size(1):
        raise RuntimeError("Even batch size 1 causes OOM.")

    low = batch_size // 2
    high = min(batch_size, max_possible)
    best = low
    while low <= high:
        mid = (low + high) // 2
        if try_batch_size(mid):
            best = mid
            low = mid + 1
        else:
            high = mid - 1

    best -=2
    if not try_batch_size(best):
        raise RuntimeError("Validation failed after finding the best batch size.")

    final_peak = torch.cuda.max_memory_allocated(device)
    print(f"Maximum feasible batch size: {best}")
    print(f"Peak memory used: {final_peak / 1024**3:.2f} GB / {allowed_memory / 1024**3:.2f} GB")
    return best