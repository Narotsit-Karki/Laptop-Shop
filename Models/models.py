import os
from datetime import datetime
from binascii import hexlify



class Laptop:
	file_path = {'Sales':"Shop_Stock.txt",'Order':"Retailer_Stock.txt"}

	def __init__(self,Id,Name,Brand,Price,Quantity,CPU_Details,GPU_Details,Image):
		self.id = Id
		self.name = Name
		self.brand = Brand
		self.price = Price
		self.quantity = Quantity
		self.cpu_details = CPU_Details
		self.gpu_details = GPU_Details
		self.image = os.path.join("assets/images/laptops/",Image)

	@classmethod
	def create_laptop(cls,format,Id):
		Name,Brand,Price,Quantity,CPU_Details,GPU_Details,Image = format.split(",")
		Price = float(Price.strip(" $"))
		return cls(Id,Name,Brand[1:],Price,int(Quantity),CPU_Details[1:],GPU_Details[1:],Image[1:].strip("\n"))

	def display_details(self):
		print(f"\n<---------------Laptop Details----------------->")
		print(f"[*] Name: {self.name}")
		print(f"[*] Brand: {self.brand}")
		print(f"[*] Price: ${self.price}")
		print(f"[*] Quantity: {self.quantity}")
		print(f"[*] Processor Details: {self.cpu_details}")
		print(f"[*] GPU Details: {self.gpu_details}")

	
	def update_quantity(self):
		raise NotImplementedError("[!] Update Quantity Function")


	def update_stock(self,file_path):
		with open(file_path,'r') as file:
			data = file.readlines()
			data[self.id] = f"{self.name}, {self.brand}, ${self.price}, {self.quantity}, {self.cpu_details}, {self.gpu_details}"
		with open(file_path,'w') as file:
			file.writelines(data)	




class Distributor:
	file_path = "Distributors.txt"
	def __init__(self,RegNo,Name,Address):
		self.regno = RegNo
		self.name = Name 
		self.address = Address

	def __str__(self):
		return f"{self.name}"

	def display_details(self):
		print(f"\n<---------------Distributor Details----------------->")
		print(f"[*] Register No: {self.regno}")
		print(f"[*] Name: {self.name}")
		print(f"[*] Address: {self.address}")

	@classmethod
	def create_distributor(cls,format):
		RegNo,Name,Address = format.split("-")
		return cls(RegNo,Name,Address)




class BaseUser:
	def __init__(self,Id,UName,isActive=True,isAdmin=False,lastloggedin=None,isLoggedIn=False):
		self.id = Id
		self.uname = UName
		self.isActive = isActive
		self.lastloggedin = lastloggedin
		self.isAdmin = isAdmin
		self.isLoggedIn=isLoggedIn


class User(BaseUser):
	def __init__(self,Id,UName,FullName,Address,Phone,Billing=None):
		super().__init__(Id,UName)
		self.fullname = FullName
		self.address = Address
		self.phone = Phone
		self.billing = Billing

	def __str__(self):
		return f"{self.fullname}"





class BaseTransaction:
	
	def __init__(self,Id,Date_Time,Total_Payment,Quantity,Laptop):
		self.id = Id
		self.date_time = Date_Time
		self.total_payment = Total_Payment
		self.quantity = Quantity
		self.laptop = Laptop

class SaleTransaction(BaseTransaction):
	shipping_cost = 50
	def __init__(self,Id,Date,Total_Payment,Type,Quantity,Customer,Laptop):
		super().__init__(Id,Date,Total_Payment,Type,Quantity,Laptop)
		self.customer = Customer
		self.billing_type = Type
	
	@classmethod
	def conduct_transaction(cls,Customer,Laptop,Quantity):
		if(Quantity <= Laptop.quantity):
			Id = hexlify(os.urandom(8)).decode()
			Date_Time = datetime.now()
			Laptop.quantity -= Quantity
			Laptop.update_stock(file_path=Laptop.file_path['Sales'])
			Total_Payment = (Quantity * Laptop.price) + cls.shipping_cost
			return cls(Id,Date_Time,Total_Payment,Customer.billing,Quantity,Customer,Laptop)
		else:
			raise("[!] Quantity Exceeded")

	
	def generate_invoice(self):
		with open(f"Transactions/Sales/sales_transaction_{self.id}.txt",'w') as file:
			transaction  = [
							"<-------Transaction Details-------->\n\n",
							f"[*] Transaction ID: {self.id}\n"
							f"[*] Laptop: {self.laptop.name}\n",
							f"[*] Brand: {self.laptop.brand}\n",
							f"[*] Customer: {self.customer.fullname}\n",
							f"[*] Purchased at: {self.date_time.strftime('%d %B, %Y -- %H:%M:%S')}\n",
							f"[*] Quantity: {self.quantity}\n"
							f"[*] Laptop Cost: ${self.laptop.price*self.quantity:,}\n",
							f"[*] Shipping Cost: ${self.shipping_cost}\n",
							f"[*] Total Payment: ${self.total_payment:,}\n"
						  ]
			file.writelines(transaction)
			

class OrderTransaction(BaseTransaction):
	vat = 0.13

	def __init__(self,Id,Date_Time,VAT,Total_Payment,Quantity,Distributor,Laptop):
		super().__init__(Id,Date_Time,Total_Payment,Quantity,Laptop)
		self.distributor = Distributor
		self.VAT = VAT

	@classmethod
	def conduct_transaction(cls,distributor,laptop,quantity):
		if(quantity <= laptop.quantity):
			Id = hexlify(os.urandom(8)).decode()
			Date_Time = datetime.now()
			
			TA_without_vat = laptop.price * quantity
			VAT = cls.vat * TA_without_vat
			Gross_Amount = VAT + TA_without_vat

			# update quantity in retailers stock
			laptop.quantity -= quantity
			laptop.update_stock(file_path=Laptop.file_path['Order'])

			#update quantity in sales stock
			with open(Laptop.file_path['Sales'],'r') as file:
				data = file.readlines()
				sales_laptop = Laptop.create_laptop(data[laptop.id],laptop.id)
				sales_laptop.quantity += quantity

			sales_laptop.update_stock(file_path=Laptop.file_path['Sales'])


			return cls(Id,Date_Time,VAT,Gross_Amount,quantity,distributor,laptop)
		else:
			raise("[!] Quantity Exceeded")


	def generate_invoice(self):
		with open(f"Transactions/Order/order_transaction_{self.id}.txt",'w') as file:
			transaction  = [
							"<-------Transaction Details-------->\n\n",
							f"[*] Transaction ID: {self.id}\n"
							f"[*] Laptop: {self.laptop.name}\n",
							f"[*] Brand: {self.laptop.brand}\n",
							f"[*] Distributor: {self.distributor.name}\n",
							f"[*] Purchased at: {self.date_time.strftime('%d %B, %Y -- %H:%M:%S')}\n",
							f"[*] Quantity: {self.quantity}\n"
							f"[*] Laptop Cost: ${self.laptop.price*self.quantity:,}\n",
							f"[*] VAT: ${self.VAT:,}\n",
							f"[*] Total Payment: ${self.total_payment:,}\n"
						  ]
			file.writelines(transaction)


