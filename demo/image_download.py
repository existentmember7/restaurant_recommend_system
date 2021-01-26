import os
from urllib.request import urlretrieve
from urllib.error import HTTPError
from urllib.error import URLError

def imageDownload( file_path , image_link ) :
    try :
        urlretrieve(image_link, file_path) #下載檔案
        # done
    except HTTPError as e :
        print( e , ':' , image_link )
    except URLError as e :
        print( e , ':' , image_link )

    return ;


if __name__ == "__main__" :
    dir_path = './'
    filename = 'test.jpg'
    image_link =  "https://media-cdn.tripadvisor.com/media/photo-s/11/1f/8a/e8/caption.jpg"
    local_path = os.path.join( dir_path + filename )  #檔案儲存位置

    imageDownload( local_path , image_link )
