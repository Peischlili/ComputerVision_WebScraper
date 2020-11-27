from packageManager import *
from buildIndex import pooling_output

# function to call on existing faiss index file, given image with certain number of neighbors
def search_index(query_image, index_file, nb_neighbors):
    # we use here faiss-cpu
    DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

    transforms_ = transforms.Compose([
        transforms.Resize(size=[224, 224], interpolation=2),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    index = faiss.read_index(index_file)
    img = Image.open(query_image)
    input_tensor = transforms_(img)
    input_tensor = input_tensor.view(1, *input_tensor.shape)
    with torch.no_grad():
        query_descriptors = pooling_output(input_tensor.to(DEVICE)).cpu().numpy()
        distance, indices = index.search(query_descriptors.reshape(1, 2048), nb_neighbors)
    print(indices)
    return indices