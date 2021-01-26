import os
import pickle
import json
import math
from image_download import imageDownload

class Demo():
    def __init__(self):
        with open("./data/inverted_file.pkl",'rb') as f:
            self.inverted_file = pickle.load(f)
        with open("./data/store_list.pkl","rb") as f:
            self.store_list = pickle.load(f)    
        with open("./data/store_length_ratio.pkl","rb") as f:
            self.store_length_ratio = pickle.load(f)
        with open("./dict/oov.pkl","rb") as f:
            self.oov = pickle.load(f)
        with open("./data/store_without_comments.pkl","rb") as f:
            self.store_without_comments = pickle.load(f)

    def get_score(self, query):
        score = {}
        doc_num = 8540
        b = 0.3
        for term in query:
            try :
                dic = self.inverted_file[term]
            except :
                print(f"{term} doesn't exist.")
                self.oov[term] = 0
                continue
            doc_freq = len(list(dic.keys()))
            idf = math.log((doc_num-doc_freq+0.5)/doc_freq+0.5)
            for store_id in dic.keys():
                store = self.store_list[store_id]
                content = self.store_without_comments[store]


                tf = dic[store_id]
                
                tf = math.log(1+math.log(1+tf,2))
                tf = tf / ( 1.-b + b * self.store_length_ratio[store_id])
                try :
                    score[store] 
                except:
                    score[store] = 0
                score[store] += tf * idf
             
        return score
    
    def get_image_path(self, img_url):
        output_img_path = []
        for i in range(len(img_url)):
            if len(img_url[i]) == 0:
                filename = './tmp.jpg'
                output_img_path.append(filename)
            else:
                filename = os.path.join('./{}.jpg'.format(i))
                imageDownload(filename, img_url[i])
                output_img_path.append(filename)
        return output_img_path

    def run_v2(self, district=None, category=None, pet=None, cp=None, service=None, vege=None):

        rating = 0
        query = []

        store_list = None
        district_store = None
        category_store = None
        pet_store = None
        vege_store = None
        if district is not None:
            district_store = self.inverted_file[district].keys()
            # query.append(district)
        if category is not None:
            category_store = self.inverted_file[category].keys()
            query.append(category)
        if pet is not None:
            pet_store = self.inverted_file[pet].keys()
            query.append(pet)
        if vege is not None:
            vege_store = self.inverted_file[vege].keys()
            query.append(vege)

        if store_list is None and district_store is not None:
            store_list = district_store
        elif district_store is not None:
            store_list &= district_store
        if store_list is None and category_store is not None:
            store_list = category_store
        elif category_store is not None:
            store_list &= category_store
        if store_list is None and pet_store is not None:
            store_list = pet_store
        elif pet_store is not None:
            store_list &= pet_store
        if store_list is None and vege_store is not None:
            store_list = vege_store
        elif vege_store is not None:
            store_list &= vege_store

        if cp is not None:
            query.append(cp)
        if service is not None:
            query.append(service)
            

        if len(query) < 1:
            print("empty query")
            return 
        score = {}
        doc_num = 8540
        b = 0.3

        
        for term in query:
            try :
                dic = self.inverted_file[term]
            except :
                print(f"{term} doesn't exist.")
                self.oov[term] = 0
                continue
            doc_freq = len(list(dic.keys()))
            idf = math.log((doc_num-doc_freq+0.5)/doc_freq+0.5)

            if store_list is not None:
                store_pool = store_list & dic.keys()
            else :
                store_pool = dic.keys()
            for store_id in store_pool:
                store = self.store_list[store_id]


                tf = dic[store_id]                
                tf = math.log(1+math.log(1+tf,2))
                tf = tf / ( 1.-b + b * self.store_length_ratio[store_id])
                try :
                    score[store] 
                except:
                    score[store] = 0
                score[store] += tf * idf
        # score = get_score(query)


        with open("./dict/oov.pkl","wb") as f:
            pickle.dump(self.oov,f)
        key_list = list(score.keys())
        value_list = list(score.values())

        answer = sorted(range(len(key_list)),key=value_list.__getitem__,reverse=True)

        output_rest = []
        output_address = []
        output_url = []
        img_url = []
        img_path = ['tmp.jpg']*5
        if len(answer) < 1:
            print("term doesn't exist")
        else:
            num = min(5,len(answer))
            for i in range(num):
                index = answer[i]
                store = key_list[index]
                output_rest.append(store)
                output_address.append(self.store_without_comments[store]['address'])
                output_url.append(self.store_without_comments[store]['href'])
                img_url.append(self.store_without_comments[store]['img_url'])
                print(store)
            img_path = self.get_image_path(img_url)
#                print(self.store_without_comments[store])

        return output_rest, output_address, output_url, img_path

    def run_v1(self, query):

        query = query.strip().split()

        if len(query) < 1:
            print("empty query")
            return 
        score = {}
        doc_num = 8540
        b = 0.3

        
        score = self.get_score(query)


        with open("./dict/oov.pkl","wb") as f:
            pickle.dump(self.oov,f)
        key_list = list(score.keys())
        value_list = list(score.values())

        answer = sorted(range(len(key_list)),key=value_list.__getitem__,reverse=True)

        output_rest = []
        output_address = []
        output_url = []
        img_url = []
        img_path = ['tmp.jpg']*5
        
        if len(answer) < 1:
            print("term doesn't exist")
        else:
            num = min(5,len(answer))
            for i in range(num):
                index = answer[i]
                store = key_list[index]
                output_rest.append(store)
                output_address.append(self.store_without_comments[store]['address'])
                output_url.append(self.store_without_comments[store]['href'])
                img_url.append(self.store_without_comments[store]['img_url'])
                print(store)
            img_path = self.get_image_path(img_url)
        

        return output_rest, output_address, output_url, img_path
if __name__ == "__main__":
    demo = Demo()
    # print(demo.inverted_file["雞排"].keys())
    # print(demo.inverted_file["珍奶"].keys())

    # print(demo.inverted_file["雞排"].keys() & demo.inverted_file["珍奶"].keys() )
    # demo.run_v2(pet="寵物友善",category="中式")

    while  True:
        query = input("search :")
        demo.run_v1(query)
