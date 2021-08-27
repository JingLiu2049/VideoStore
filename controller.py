from modles import *


class VideoShop:
    def __init__(self) :
        self.videos={}
        self.customers={}

    # verify data type and create a vedio object
    def createVideo(self,title:str,year:str,availability:bool=True):
        if isinstance(title,str) and isinstance(year,str) and isinstance(availability,bool):
            newVideo = Video(title,year,availability)
            self.videos.setdefault(newVideo.id,newVideo)
        else:
            raise TypeError('parameters type error')

    # verify data type and create a customer object
    def createCustomer(self,name:str,city:str,payment:float=0):
        if isinstance(name,str) and isinstance(city,str) and isinstance(payment,float):
            newCustomer= Customer(name,city,payment)
            self.customers.setdefault(newCustomer.id,newCustomer)
        else:
            raise TypeError('parameters type error')

    # rent a video to a customer
    def renting(self,customerId:int,videoId:int):
        customer = self.customers.get(customerId)
        video = self.videos.get(videoId)
        if video and customer:
            try:
                video.setRenting(customer)
            except VideoError as ve:
                print(ve.__class__,ve)
                response = MyResponse(0,ve.msg)
            else:
                try:
                    customer.setRenting(video)
                except CustomerError as ce:
                    print(ce.__class__,ce)
                    response = MyResponse(0,ce.msg)
                else:
                    response = MyResponse(1,"Renting operation is completed.")
        else:
            error = 'Video' if customer else 'Customer'
            response = MyResponse(0,f"Invalid {error}, pelase check and try again.")
        return response
    
    # return a video from a customer
    def returning(self,customerId:int,videoId:int):
        customer = self.customers.get(customerId)
        video = self.videos.get(videoId)
        if video and customer:
            try:
                customer.setReturning(video)
            except CustomerError as ce:
                print(ce.__class__,ce)
                response = MyResponse(0,ce.msg)
            else:
                try:
                    video.setReturning(customer)
                except VideoError as ve:
                    print(ve.__class__,ve)
                    response = MyResponse(0,ve.msg)
                else:
                    response = MyResponse(1,"Returning operation is completed.")
        else:
            error = 'Video' if customer else 'Customer'
            response = MyResponse(0,f"Invalid {error}, pelase check and try again.")
        return response
    
    # get detail information of a video
    def showVideoInfo(self,videoId:int):
        video = self.videos[videoId]
        return video.showDetail()

    # get detail information of a customer
    def showCustomerInfo(self,customerId:int):
        customer = self.customers[customerId]
        return  customer.showDetail()

    # return operation based on video's status
    def getOperation(self,customerId,videoId):
        customer= self.customers[customerId]
        video = self.videos[videoId]
        if video.availability:
            return 'rent'
        elif video.checkRentalRecord(customer):
            return 'return'
        else:
            return 'na'


# below are functions to create controller instence
# *********************************************************************
# a function used to get data from files
def getFileData(filename):
    args = []
    with open(filename) as videos:
        data = videos.read().splitlines()
        for i in data:
            arg = i.split(',')
            for j in range(len(arg)):
                arg[j] = arg[j].strip()
            args.append(arg)
    return args

# a function to create VideoShop object with data from a file
def getVideoShopController():
    vs = VideoShop()
    try:
        videoData = getFileData('Video.txt')
        for i in videoData:
            i[2] = True if i[2].lower()=='true' else False
            vs.createVideo(*i)
        customerData = getFileData('Customer.txt')
        for i in customerData:
            i[2] = float(i[2])
            vs.createCustomer(*i)
    except Exception as e:
        print(e.__class__,e)
    return vs



                
