




import numpy as np
import rasterio
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from sklearn.neighbors import KNeighborsClassifier

def cluster_image(imagery_fp, cluster_type='kmeans', n_clusters=5, visualize=True):
    """
    Realiza clustering en una imagen satelital utilizando diferentes algoritmos.
    
    Parámetros:
    imagery_fp (str): Ruta al archivo de imagen satelital (.tif)
    cluster_type (str): Tipo de clustering a utilizar ('kmeans', 'gmm', 'knn', o 'all')
    n_clusters (int): Número de clusters a generar
    visualize (bool): Si se debe visualizar el resultado
    
    Retorna:
    dict: Diccionario con las imágenes procesadas y las etiquetas
    """
    # Abrir la imagen
    img_file = rasterio.open(imagery_fp)
    img = img_file.read()
    
    # Reformar la imagen para clustering
    pixels = img.reshape(img.shape[0], img.shape[1] * img.shape[2]).T
    
    # Definir una máscara para identificar los píxeles de fondo
    # Un píxel se considera de fondo si todos sus valores en todos los canales son 0
    mascara = np.any(pixels != 0, axis=1)
    
    # Filtrar los píxeles que no son de fondo
    pixels_filtrados = pixels[mascara]
    
    results = {}
    
    # Función para crear la imagen clusterizada
    def create_clustered_image(labels):
        clustered_image = np.full((img.shape[1], img.shape[2]), -1)  # -1 para fondo
        clustered_image[mascara.reshape(img.shape[1], img.shape[2])] = labels
        return clustered_image
    
    # Aplicar K-means si se solicita
    if cluster_type.lower() == 'kmeans' or cluster_type.lower() == 'all':
        kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(pixels_filtrados)
        labels_filtrados_kmeans = kmeans.labels_
        clustered_image_kmeans = create_clustered_image(labels_filtrados_kmeans)
        results['kmeans'] = {
            'image': clustered_image_kmeans,
            'labels': labels_filtrados_kmeans,
            'model': kmeans
        }
    
    # Aplicar Gaussian Mixture Model si se solicita
    if cluster_type.lower() == 'gmm' or cluster_type.lower() == 'all':
        gmm = GaussianMixture(n_components=n_clusters)
        gmm.fit(pixels_filtrados)
        labels_filtrados_gmm = gmm.predict(pixels_filtrados)
        clustered_image_gmm = create_clustered_image(labels_filtrados_gmm)
        results['gmm'] = {
            'image': clustered_image_gmm,
            'labels': labels_filtrados_gmm,
            'model': gmm
        }
    
    # Aplicar K-Nearest Neighbors si se solicita
    if cluster_type.lower() == 'knn' or cluster_type.lower() == 'all':
        # Para KNN necesitamos etiquetas de entrenamiento, usamos K-means si no están disponibles
        if 'kmeans' not in results:
            kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(pixels_filtrados)
            train_labels = kmeans.labels_
        else:
            train_labels = results['kmeans']['labels']
            
        knn = KNeighborsClassifier(n_neighbors=n_clusters)
        knn.fit(pixels_filtrados, train_labels)
        labels_filtrados_knn = knn.predict(pixels_filtrados)
        clustered_image_knn = create_clustered_image(labels_filtrados_knn)
        results['knn'] = {
            'image': clustered_image_knn,
            'labels': labels_filtrados_knn,
            'model': knn
        }
    
    if visualize and results:
        n_plots = len(results)
        fig, axs = plt.subplots(1, n_plots, figsize=(5*n_plots, 7))
        
        if n_plots == 1:
            method = list(results.keys())[0]
            axs.imshow(results[method]['image'], cmap='jet')
            axs.axis('off')
            axs.set_title(method.upper())
        else:
            for i, method in enumerate(results.keys()):
                axs[i].imshow(results[method]['image'], cmap='jet')
                axs[i].axis('off')
                axs[i].set_title(method.upper())
        
        plt.show()
    
    return results

# Ejemplo de uso:
results = cluster_image('/home/agrosavia/Documents/rs_agrosavia/DATA_CUBE_AGROSAVIA/ROI/GIS_FEDEPANELA/5.RECORTES/464_moniquira/1687.0/STACK/stack_ndvi.tif', cluster_type='all', n_clusters=5)
#results_kmeans = cluster_image('/home/agrosavia/Documents/rs_agrosavia/DATA_CUBE_AGROSAVIA/ROI/GIS_FEDEPANELA/for_real/363.0/STACK/stack_ndvi.tif', cluster_type='kmeans')
#results_gmm = cluster_image('/home/cristianrr/Geo_Agro/for_real/363.0/STACK/stack_ndvi.tif', cluster_type='gmm', n_clusters=7)