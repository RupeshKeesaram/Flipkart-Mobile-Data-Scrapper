from bs4 import BeautifulSoup as bs
import requests
import lxml


def web_scrapper(mobile_name,count):
    '''

    :param mobile_name:
    :return: dictionary containing mobile details.

    '''

    # flipkart base url
    base_url = "https://www.flipkart.com/search?q="
    mobile_name = mobile_name.replace(" ", "")

    # inside try function we are gonna try to get a request response from flipkart and collect all mobile details.
    try:

        # requesting a response using bs4
        main_page_respone = requests.get(base_url + mobile_name)

        # extracting text from the response
        main_page_content = main_page_respone.text

        # creating an BeautifulSoup object with main_page_content
        main_page_html = bs(main_page_content, "lxml")
        # collecting mobiles and <a> tags to navigate in deeper
        prod_names = main_page_html.findAll("div", class_="_4rR01T")
        prod_a_tags = main_page_html.findAll("a", class_="_1fQZEK")
        cost_lists = main_page_html.findAll("div", class_="_30jeq3 _1_WHN1")

        if len(prod_names) > 0:

            product_links = []
            for a_tag, cost in zip(prod_a_tags, cost_lists):

                # finding the cost of the mobile and converting it into integer
                cost = int("".join(cost.text[1:].split(",")))

                if cost > 8000:
                    product_links.append(base_url + a_tag["href"])


            # selecting only top 5 mobiles
            product_links = product_links[:count]
            mobile_details = []

            for i in range(count):

                # printing mobile links
                # print("Product Link: ", link)

                try:
                    prod_results = requests.get(product_links[i])
                    prod_content = prod_results.text
                    prod_soup = bs(prod_content, "lxml")
                except:
                    return "Error occured while dealing with individual mobile details, Pls try with some other mobile name"

                # different classes collected from flipKart, which are used to extract mobile details.

                mobile_rating_class = "_2d4LTz"
                cost_class = '_30jeq3 _16Jk6d'
                rating_class = "_3LWZlK"
                reviews_class = "_2_R_DZ"
                features_class = "_21Ahn-"
                parts_rating_class = "_2Ix0io"
                offers_class = "_16eBzU col"
                review_class = "_2-N8zT"
                reviewed_cust_name_class = "_2sc7ZR _2V5EHH"
                image_class = "CXW8mj _3nMexc"

                try:
                    product_name= prod_names[i].text.split("(")[0]
                    prod_color= prod_names[i].text.split("(")[-1].split(",")[0].split()[-1]
                    feature_responses = prod_soup.findAll("li", class_=features_class)
                    product_cost = prod_soup.find("div", class_=cost_class).text
                    product_rating = prod_soup.find("div", class_=rating_class).text
                    product_total_ratings = (prod_soup.find("span", class_=reviews_class).text.split("&")[0]).split()[0]
                    product_total_reviews = \
                    (prod_soup.find("span", class_=reviews_class).text.split("&")[1].strip()).split()[0]
                    product_part_responses = prod_soup.findAll("text", class_=parts_rating_class)
                    offer_detail_responses = prod_soup.findAll("li", class_=offers_class)
                    product_review_responses = prod_soup.findAll("p", class_=review_class, limit=3)
                    product_cust_name_responses = prod_soup.findAll("p", class_=reviewed_cust_name_class, limit=3)

                    # collecting image source link and deleting content after ? in link
                    mobile_image=prod_soup.find("div",class_=image_class).find("img")["src"].split("?")[0]

                except:
                    return "Error occured while scrapping mobile features, pls tryout with another mobile name"

                product_part_names = ["Camera", "Battery", "Display", "Value For Money"]
                product_parts_rating = []

                if product_parts_rating != None:
                    for i in product_part_responses:
                        product_parts_rating.append(i.text)
                else:
                    product_parts_rating = ["Counld't able to find rating of individual parts"] * 4

                product_features = []
                if feature_responses != None:
                    for i in feature_responses:
                        product_features.append(i.text)
                else:
                    product_features = ["Couldn't find any features"]

                product_offers = []
                if offer_detail_responses != None:
                    for i in offer_detail_responses:
                        product_offers.append(i.find_all("span", class_=False)[0].text)
                else:
                    product_offers = ["Couldn't able to find any offers for this mobile"]

                product_reviews = []
                product_review_cust_name = []
                if product_review_responses != None:
                    for i in range(len(product_review_responses)):
                        try:
                            cust_review = product_review_responses[i].text
                        except Exception:
                            cust_name = "No reviews"
                        try:
                            cust_name = product_cust_name_responses[i].text
                        except:
                            cust_name = "Anonymous"

                        product_reviews.append(cust_review)
                        product_review_cust_name.append(cust_name)

                else:
                    product_review_responses = ["Couldn't able to find any review responses"]

                """
                print("Mobile name :", product_name)
                print("Mobile Cost :", product_cost)

                print("--" * 50)

                print("Mobile rating : ", product_rating)
                for key, value in zip(product_part_names, product_parts_rating):
                    print(key, "rating :", value)

                print("Total Ratings ", product_total_ratings)
                print("Total Reviews ", product_total_reviews)

                print("--" * 50)

                print("Product Features are as follows : \n")
                for feature in product_features:
                    print("*", feature)

                print("--" * 50)

                print("More about Offers : ")
                for offer in product_offers:
                    print("*", offer)

                print("-" * 100)

                print("More about reviews :")
                print()
                for i in product_reviews:
                    print(i)
                    print("*" * 100)

                """

                results = {
                    "image":[mobile_image,prod_color],
                    "basic_info": {"Name": product_name, "Cost": product_cost,
                                   "Rating": product_rating},
                    "rating_details": dict(zip(product_part_names, product_parts_rating)),
                    "total_reviews_costs": {"Total_Ratings": product_total_ratings,
                                            "Total_Reviews": product_total_reviews},
                    "product_features": dict(zip([i for i in range(1, len(product_features) + 1)], product_features)),
                    "product_offers": dict(zip([i for i in range(1, len(product_offers) + 1)], product_offers)),
                    # "product_reviews": dict(zip(product_review_cust_name, product_reviews)),
                }
                mobile_details.append(results)
        else:
            return "Can't able to extract any mobile data, pls try another mobile name"
        return mobile_details
    except Exception as e:
        return "Looks like something went wrong " + e

