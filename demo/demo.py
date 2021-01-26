import pickle 
import json
import math

def get_score(query, inverted_file, name_list, name_length_ratio, oov,  name_without_comments,
            district="None", price_floor="None", price_ceiling="None", rating=0):
    score = {}
    doc_num = 8000
    b = 0.3
    for term in query:
        try :
            dic = inverted_file[term]
        except :
            print(f"{term} doesn't exist.")
            oov[term] = 0
            continue
        doc_freq = len(list(dic.keys()))
        idf = math.log((doc_num-doc_freq+0.5)/doc_freq+0.5)
        for name_id in dic.keys():
            name = name_list[name_id]
            content = name_without_comments[name]
            if district != "None" and district != content["district"]:
                continue

            if price_floor != "None" and price_floor < float(content["avg_price"]):
                continue
            
            if price_ceiling != "None" and price_ceiling > float(content["avg_price"]):
                continue
            if rating > float(content["rating"]):
                continue
            tf = dic[name_id]
            tf = math.log(1+math.log(1+tf,2))
            tf = tf / ( 1.-b + b * name_length_ratio[name_id])
            try :
                score[name] 
            except:
                score[name] = 0
            score[name] += tf * idf


    return score

def main():
    
    with open("./data/inverted_file.pkl",'rb') as f:
        inverted_file = pickle.load(f)
    with open("./data/name_list.pkl","rb") as f:
        name_list = pickle.load(f)    
    with open("./data/name_length_ratio.pkl","rb") as f:
        name_length_ratio = pickle.load(f)
    # with open("./data/zhongzheng/inverted_file.pkl",'rb') as f:
    #     zhongzheng_inverted_file = pickle.load(f)
    # with open("./data/zhongzheng/name_list.pkl","rb") as f:
    #     zhongzheng_name_list = pickle.load(f)    
    # with open("./data/zhongzheng/name_length_ratio.pkl","rb") as f:
    #     zhongzheng_name_length_ratio = pickle.load(f)
    with open("./dict/oov.pkl","rb") as f:
        oov = pickle.load(f)

    with open("./data/name_without_comments.pkl","rb") as f:
        name_without_comments = pickle.load(f)

    while True:
        query = input("search term: ")
        if query == "exit":
            break
        query = query.strip().split()
        if len(query) <1:
            print("invalid query")
            continue   

        district = input("district: ")
        # district = "None"
        # price_range = input("price range: ").strip().split()
        rating = input("rating: ")
        try :
            rating = float(rating)
        except:
            print("invalid rating, set rating = 0")
            rating = 0
 

        score = get_score(query, inverted_file, name_list, name_length_ratio, oov, name_without_comments, district=district,
                             rating=rating)
        # zhongzheng_score = get_score(query, zhongzheng_inverted_file, zhongzheng_name_list, zhongzheng_name_length_ratio, oov)
        # score = {}
        # score.update(daan_score)
        # score.update(zhongzheng_score)
        # district = query[0]
        # query = query[1:]
        # if district == '0':
        #     daan_score = get_score(query, daan_inverted_file, daan_name_list, daan_name_length_ratio)
        #     zhongzheng_score = get_score(query, zhongzheng_inverted_file, zhongzheng_name_list, zhongzheng_name_length_ratio)
        #     score = {}
        #     score.update(daan_score)
        #     score.update(zhongzheng_score)
        # else:
        #     if district == '1':
        #         score = get_score(query, daan_inverted_file, daan_name_list, daan_name_length_ratio)
        #     else:
        #         score = get_score(query, zhongzheng_inverted_file, zhongzheng_name_list, zhongzheng_name_length_ratio)

        with open("./dict/oov.pkl","wb") as f:
            pickle.dump(oov,f)
        key_list = list(score.keys())
        value_list = list(score.values())

        answer = sorted(range(len(key_list)),key=value_list.__getitem__,reverse=True)

        if len(answer) < 1:
            print("term doesn't exist")
        else:
            num = min(5,len(answer))
            for i in range(num):
                index = answer[i]
                name = key_list[index]
                print(name, value_list[index])
                print(name_without_comments[name])


if __name__ == "__main__":
    main()