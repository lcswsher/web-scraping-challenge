# import necessary libraries
from flask import Flask, render_template, redirect

# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
from flask_pymongo import PyMongo

# import python script converted from "mission_to_mars.ipynb" to "scrape_mars.py" 
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

# Pymongo connects to the MongoDB server running on port 27017 on localhost database "mars_app"
app.config['MONGO_URI'] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# create route that renders the index.html template
@app.route("/")
def index():
    
    mars_information = mongo.db.mars_information.find_one()
    
    return render_template("index.html", mars_information=mars_information)


# create route that renders index.html template (updating Mongodb with scraped mars_information)
@app.route('/scrape')
def scrape():
    
    mars_information = scrape_mars.scrape()
    
    # mars_data = scrape_mars.scrape_information()
    
    mongo.db.mars_information.update_one({}, mars_information, upsert=True)
    
    return redirect("/")
    # return render_template("index.html", text="Serving up cool text from the Flask server!!")


if __name__ == "__main__":
    app.run(debug=True)
