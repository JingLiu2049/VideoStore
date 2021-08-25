from flask import Flask, render_template, redirect, request, Response, jsonify
from controller import getVideoShopController,MyResponse


app = Flask(__name__)

vs = getVideoShopController()

# send videos and customers to frontend for displaying
@app.route('/')
def videoShop():
    return render_template('home.html',videos = vs.videos,customers = vs.customers)

# deal the request of showing details for customer and video
# also send video status for front-end side to disable buttons 
@app.route('/detail',methods = ['POST'])
def showDetail():
    customerID = request.form.get('customer')
    videoID = request.form.get('video')
    try:
        customerInfo = vs.showCustomerInfo(int(customerID)) if customerID else ''
        videoInfo = vs.showVideoInfo(int(videoID)) if videoID else ''
        operation = None
        if customerID and videoID:
            operation = vs.getOperation(int(customerID),int(videoID))
    except Exception as e:
        print(e.__class__,e)
        response = MyResponse(0,msg="Your connection is unstable, please try later.")
    else:
        response = MyResponse(1,data={'customer':customerInfo,'video':videoInfo,'operation':operation})
    return jsonify(response.__dict__)

# deal with request of renting a video to a customer
@app.route('/rent',methods = ['POST'])
def renting():
    try:
        customerID = int(request.form.get('customer'))
        videoID = int(request.form.get('video'))
        response = vs.renting(customerID,videoID)
    except TypeError as te:
        print(te)
        response = MyResponse(0,msg="You have to choose both a Customer and a Movie.")
    except Exception as e:
        print(e.__class__,e)
        response = MyResponse(0,msg="Your connection is unstable, please try later.")
    return jsonify(response.__dict__)

# deal with request of returning a video rented by a customer
@app.route('/return',methods = ['POST'])
def returning():
    try:
        customerID = int(request.form.get('customer'))
        videoID = int(request.form.get('video'))
        response = vs.returning(customerID,videoID)
    except TypeError as te:
        print(te)
        response = MyResponse(0,msg="You have to choose both a Customer and a Movie.")
    except Exception as e:
        print(e.__class__,e)
        response = MyResponse(0,msg="Your connection is unstable, please try later.")
    return jsonify(response.__dict__)

if __name__ == '__main__':
    Flask.run(app,debug=True)