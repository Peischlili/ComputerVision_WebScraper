from packageManager import *

# this command enables us to download torch models
ssl._create_default_https_context = ssl._create_unverified_context

class ImageFolderWithPaths(datasets.ImageFolder):
    """Custom dataset that includes image file paths. Extends torchvision.datasets.ImageFolder
    """
    # override the __getitem__ method
    # __getitem__ method is the method that dataloaders calls
    def __getitem__(self, index):
        # this is what ImageFolder normally returns
        original_tuple = super(ImageFolderWithPaths, self).__getitem__(index)
        # Image file path
        path = self.imgs[index][0]
        # Make a tuple that includes original and the path
        tuple_with_path = (original_tuple + (path,))
        return tuple_with_path

# function to extract features
def pooling_output(x):
    global model
    for layer_name, layer in model._modules.items():
        x = layer(x)
        if layer_name == 'avgpool':
            break
    return x

# Transforms are made using the torchvision.transforms library.
# transforms.Compose allows to compose multiple transforms together so we can use more than one transformation.
# resizes the images to 224 x 224 (input size required by the ResNet)
# transforms.ToTensor() converts image into numbers.
# transforms.Normalize() subtracts the mean from each value and then divides by the standard deviation
transforms_ = transforms.Compose([
    transforms.Resize(size=[224, 224], interpolation=2),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Load in each dataset and apply transformations using the torchvision.datasets as datasets library
# data_dir main directory containing our image dataset
data_dir = "/Users/peisch/code/WebScraper/ImageSearch/images"
dataset = ImageFolderWithPaths(data_dir, transforms_)
dataloader = torch.utils.data.DataLoader(dataset, batch_size=1)

# use GPU if possible => here we use faiss-cpu
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
# Get pretrained model using torchvision.models
model = models.resnet50(pretrained=True)

# iterate over data
# image_paths is to be saved since it contains information on index
image_paths = []
# descriptors: list of output vectors
descriptors = []
model.to(DEVICE)

# Tell torch not to calculate gradients
with torch.no_grad():
    model.eval()
    for inputs, labels, paths in dataloader:
        result = pooling_output(inputs.to(DEVICE))
        descriptors.append(result.cpu().view(1, -1).numpy())
        image_paths.append(paths)
        torch.cuda.empty_cache()

# build faiss index with fixed size
index = faiss.IndexFlatL2(2048)
# stack arrays in sequence vertically (row wise).
descriptors = np.vstack(descriptors)
index.add(descriptors)
faiss.write_index(index, f"{data_dir}/faiss_index")