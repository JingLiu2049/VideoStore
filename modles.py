
class Video:
    ID =100000
    RENTAL_PRICE = 2
    def __init__(self,title,year,availability=True):
        Video.ID += 1
        self.__id = Video.ID
        self.__title = title
        self.__year = year
        self.__availability = availability
        self.__currentCustomer = None
        self.__history = []
    
    
    @property
    def id(self):
        return self.__id

    @property
    def title(self):
        return self.__title
    @title.setter
    def title(self,title):
        self.__title = title

    @property
    def year(self):
        return self.__year
    @year.setter
    def year(self,year):
        self.__year=year
    
    @property
    def availability(self):
        return self.__availability

    @property
    def currentCustomer(self):
        return self.__currentCustomer

    @property
    def history(self):
        return self.__history
    
    # create detail information for a video 
    def showDetail(self):
        available = "Available" if self.__availability else "Not Available"
        return f'{self.__title} {self.__year} {available}'

    # check if this video is rented by a customer
    def checkRentalRecord(self,customerObj):
        return self.currentCustomer.id == customerObj.id
         
    # update instance fileds when it is rented by a customer
    def setRenting(self, customerObj):
        if self.__availability:
            self.__currentCustomer = customerObj
            self.__availability = False
        else:
            raise VideoError(f'Video {self.__title} is not Available.')
    
    # update instance fileds when it is returned by a customer
    def setReturning(self, customerObj):
        if self.checkRentalRecord(customerObj):
            self.__currentCustomer = None
            self.__history.append(customerObj)
            self.__availability = True
        else:
            raise VideoError(f'Video {self.title} was not rented \
                by {customerObj.name}, please check and try again!.')




class Customer:
    ID = 100000
    def __init__(self,name, city,payment = 0.0 ):
        Customer.ID += 1
        self.__id = Customer.ID
        self.__name = name
        self.__city = city
        self.__currentVideos = []
        self.__history = []
        self.__payment =payment

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self,name):
        self.__name = name

    @property
    def city(self):
        return self.__city
    @city.setter
    def city(self,city):
        self.__city = city

    @property
    def currentVideos(self):
        return self.__currentVideos
    @property
    def payment(self):
        return self.__payment

    
    @property
    def history(self):
        return self.__history

    # a private method to count payment and update __payment field
    def __setPayment(self):
        self.__payment =len(self.__currentVideos) * Video.RENTAL_PRICE
    
    # create detail infomation for a customer
    def showDetail(self):
        personalStr = f" Customer Name: {self.name} \n City: {self.city}"
        videoStr = "Videos Rented:"
        if self.currentVideos:
            for i in self.currentVideos:
                videoStr += f' \n {i.title} '
        self.__setPayment()
        paymentStr = f'Total Payment: ${self.__payment}'
        return(
            f'{personalStr} \n \n {videoStr} \n \n {paymentStr}'
        )

    # check if a video  is rented by this customer
    def checkRentalRecord(self,videoObj):
        theVideo = [i for i in self.currentVideos if i.id == videoObj.id]
        return bool(theVideo)

    # update instance fileds when it is renting a video
    def setRenting(self, videoObj):
        if not self.checkRentalRecord(videoObj):
            self.__currentVideos.append(videoObj)
            self.__setPayment()
        else:
            raise CustomerError(f"This video is already in cutomer {self.__name}'s rental list." )
    
    # update instance fileds when it is returning a video
    def setReturning(self, videoObj):
        if self.checkRentalRecord(videoObj):
            self.__currentVideos.remove(videoObj)
            self.__history.append(videoObj)
        else:
            raise CustomerError(f'No rental record of {videoObj.title} for Customer {self.__name} .')


# class used to create response for fron-end request
class MyResponse:
    def __init__(self,status,msg='',data='') -> None:
        self.status = status
        self.msg = msg
        self.data = data
    
# two error classes to determine which class causes the error
class CustomerError(Exception):
    def __init__(self, msg) -> None:
        super().__init__(msg)
        self.msg = msg
class VideoError(Exception):
    def __init__(self, msg) -> None:
        super().__init__(msg)
        self.msg = msg


