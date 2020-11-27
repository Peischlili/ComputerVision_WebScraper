from packageManager import *
from similaritySearch import search_index


app = Flask(__name__)

# the folder to store uploaded user images
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# the folder contains faiss index file and dataset
index_folder = 'bdd/batch06'
dataset_folder = 'dataset_images'


# the main route of the application
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['image']
    if uploaded_file.filename != '':
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(filepath)
        return render_template('index.html', filename=uploaded_file.filename)

@app.route('/image/<filename>')
# display output image
def display_image(filename):
    return redirect(url_for('static', filename='images/' + filename))

@app.route('/search/<filename>/<list_index>')
# take output image, search k neighbors and return the nth one
def search_neighbor(filename, list_index):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    # indices gives the k nearest neighbors
    indices = search_index(filepath, f"{index_folder}/faiss_index", 4)
    # image_index follows the order the dataset images go through the ResNet50 with Faiss
    image_index = indices[0][int(list_index)]
    df = pd.read_csv('bdd/batch06/image_paths.csv')
    image_name = df.iloc[image_index]['image_id']
    return redirect(url_for('static', filename='database_images/' + image_name))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)