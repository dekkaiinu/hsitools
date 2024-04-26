from typing import Any, Callable, Optional, Tuple, Union

import numpy as np
import torch
import torch.utils.data as data
from sklearn.preprocessing import LabelEncoder

class HSPixelDataset(data.Dataset):
    '''
    
    '''
    def __init__(self, data, target):
        super().__init__()
        self.data = data
        self.target = target

        self.label_encoder = LabelEncoder()
        if len(self.target.shape) > 1:
            self.target = self.target[:, 0]
        self.target = self.label_encoder.fit_transform(self.target)

    def __getitem__(self, index: int) -> Tuple[Any, Any]:
        '''
        '''
        hs_pixel, target = self.data[index, :], np.array(self.target[index])

        hs_pixel = torch.from_numpy(hs_pixel).type(torch.float32)
        target = torch.from_numpy(target).type(torch.LongTensor)

        return hs_pixel, target

    def __len__(self) -> int:
        return len(self.target)
    
    