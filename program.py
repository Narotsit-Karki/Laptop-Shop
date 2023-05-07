from Models import *

# Laptops = []
# with open(Laptop.file_path['Order']) as file:
# 	for index,line in enumerate(file,start=0):
# 		laptop = Laptop.create_laptop(line,index)
# 		Laptops.append(laptop)


# user = User(1,"Narotsitk","Narotsit Karki","Baluwatar, Kathmandu",'9840418556','credit-card')

# trn1 = SaleTransaction.conduct_transaction(user,Laptops[0],10)
# trn1.generate_invoice()

# Distributors = []
# with open(Distributor.file_path,'r') as file:
# 	for line in file:
# 		distributor = Distributor.create_distributor(line)
# 		Distributors.append(distributor)
#
#
# trn1 =  OrderTransaction.conduct_transaction(Distributors[4],Laptops[7],400)
# trn1.generate_invoice()
from Interface.main import App
if __name__ == "__main__":
	App().run()