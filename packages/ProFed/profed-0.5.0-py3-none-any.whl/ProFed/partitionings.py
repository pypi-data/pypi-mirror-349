import math
import torch
import random
import numpy as np
from torchvision import datasets, transforms
from torch.utils.data import Subset, Dataset, random_split

class Partitioner:

    def partition(self, partitioning_method: str, dataset: Subset, areas: int) -> dict[int, list[int]]:
        """
        Splits a torch Subset following a given method.
        Implemented methods for label skewness are: IID, Hard, Dirichlet
        :param partitioning_method: a string containing the name of the partitioning method.
        :param dataset: a torch Subset containing the dataset to be partitioned.
        :param areas: the number of sub-areas.
        :return: a dict in which keys are the IDs of the subareas and the values are lists of IDs of the instances of the subarea
            (IDs references the original dataset).
        """
        if partitioning_method == 'Dirichlet':
            partitions = self.__partition_dirichlet(dataset, areas)
        elif partitioning_method == 'Hard':
            partitions = self.__partition_hard(dataset, areas)
        elif partitioning_method == 'IID':
            partitions = self.__partition_iid(dataset, areas)
        else:
            raise Exception(f'Partitioning method {partitioning_method} not supported! Please check :)')

        return partitions
    
    def subregions_distributions_to_devices_distributions(self, partitioning: dict[int, list[int]], mapping_devices_subregion: dict[int, list[int]], dataset: Subset) -> dict[int,Subset]:
        """
        :param partitioning: The mapping between subregions and instances.
        :param devices_for_subregion: The number of devices for each subregion.
        :param dataset: A torch Subset containing the dataset to be partitioned.
        :return: a dict in which keys are the IDs of the devices and the values are the respective Subsets.
        """
        device_to_subset = {}
        for id, indexes in partitioning.items():
            devices_in_subregion = mapping_devices_subregion[id]
            n_devices = len(devices_in_subregion)
            split = np.array_split(indexes, n_devices)
            for i, indexes in enumerate(split):
                device_to_subset[devices_in_subregion[i]] = Subset(dataset.dataset, indexes)
        return device_to_subset

    def download_dataset(self, dataset_name: str, train: bool = True, transform: transforms.Compose = None, download_path: str = 'dataset') -> Dataset:
        """
        Download the specified dataset from torchvision.
        Valid datasets are: MNIST, FashionMNIST, Extended MNIST, CIFAR10, CIFAR100.
        :param dataset_name: The dataset to be downloaded.
        :param train: Whether to download the training set or the test set.
        :param transform: Transformations that will be applied to the dataset. If none only ToTensor will be applied.
        :param download_path: The path where the dataset will be downloaded.
        :return: the specified dataset.
        """
        if transform is None:
            transform = transforms.Compose([transforms.ToTensor()])

        if dataset_name == 'MNIST':
            dataset = datasets.MNIST(root=download_path, train=train, download=True, transform=transform)
        elif dataset_name == 'CIFAR10':
            dataset = datasets.CIFAR10(root=download_path, train=train, download=True, transform=transform)
        elif dataset_name == 'CIFAR100':
            dataset = datasets.CIFAR100(root=download_path, train=train, download=True, transform=transform)
        elif dataset_name == 'EMNIST':
            dataset = datasets.EMNIST(root=download_path, split='letters', train=train, download=True, transform=transform)
        elif dataset_name == 'FashionMNIST':
            dataset = datasets.FashionMNIST(root=download_path, train=train, download=True, transform=transform)
        else:
            raise Exception(f'Dataset {dataset_name} not supported! Please check :)')
        return dataset

    def train_validation_split(self, dataset: Dataset, train_percentage: float) -> tuple[Subset, Subset]:
        """
        Split a given dataset in training and validation set.
        :param dataset: The dataset to be split in training and validation subsets.
        :param train_percentage: The percentage of training instances, it must be a value between 0 and 1.
        :return: A tuple containing the training and validation subsets.
        """
        dataset_size = len(dataset)
        training_size = int(dataset_size * 0.8)
        validation_size = dataset_size - training_size
        training_data, validation_data = random_split(dataset, [training_size, validation_size])
        return training_data, validation_data

    def __partition_hard(self, data, areas) -> dict[int, list[int]]:
        labels = len(data.dataset.classes)
        labels_set = np.arange(labels)
        split_classes_per_area = np.array_split(labels_set, areas)
        distribution = np.zeros((areas, labels))
        for i, elems in enumerate(split_classes_per_area):
            rows = [i for _ in elems]
            distribution[rows, elems] = 1 / len(elems)
        return self.__partition_by_distribution(distribution, data, areas)

    def __partition_iid(self, data, areas) -> dict[int, list[int]]:
        labels = len(data.dataset.classes)
        percentage = 1 / labels
        distribution = np.zeros((areas, labels))
        distribution.fill(percentage)
        return self.__partition_by_distribution(distribution, data, areas)

    def __partition_by_distribution(self, distribution: np.ndarray, data: Subset, areas: int) -> dict[int, list[int]]:
        indices = data.indices
        targets = data.dataset.targets
        class_counts = torch.bincount(targets[indices])
        class_to_indices = {}
        for index in indices:
            c = targets[index].item()
            if c in class_to_indices:
                class_to_indices[c].append(index)
            else:
                class_to_indices[c] = [index]
        max_examples_per_area = int(math.floor(len(indices) / areas))
        elements_per_class = torch.floor(torch.tensor(distribution) * max_examples_per_area).to(torch.int)
        partitions = {a: [] for a in range(areas)}
        for area in range(areas):
            elements_per_class_in_area = elements_per_class[area, :].tolist()
            for c in sorted(class_to_indices.keys()):
                elements = min(elements_per_class_in_area[c], class_counts[c].item())
                selected_indices = random.sample(class_to_indices[c], elements)
                partitions[area].extend(selected_indices)
        return partitions
        pass

    def __partition_dirichlet(self, data, areas):
        # Implemented as in: https://proceedings.mlr.press/v97/yurochkin19a.html
        min_size = 0
        indices = data.indices
        targets = data.dataset.targets
        N = len(indices)
        class_to_indices = {}
        for index in indices:
            c = targets[index].item()
            if c in class_to_indices:
                class_to_indices[c].append(index)
            else:
                class_to_indices[c] = [index]
        partitions = {a: [] for a in range(areas)}
        while min_size < 10:
            idx_batch = [[] for _ in range(areas)]
            for k in sorted(class_to_indices.keys()):
                idx_k = class_to_indices[k]
                np.random.shuffle(idx_k)
                proportions = np.random.dirichlet(np.repeat(0.5, areas))
                ## Balance
                proportions = np.array([p * (len(idx_j) < N / areas) for p, idx_j in zip(proportions, idx_batch)])
                proportions = proportions / proportions.sum()
                proportions = (np.cumsum(proportions) * len(idx_k)).astype(int)[:-1]
                idx_batch = [idx_j + idx.tolist() for idx_j, idx in zip(idx_batch, np.split(idx_k, proportions))]
                min_size = min([len(idx_j) for idx_j in idx_batch])
        for j in range(areas):
            np.random.shuffle(idx_batch[j])
            partitions[j] = idx_batch[j]
        return partitions