def main():

	multi_transfer = []

	token_decimals = eval(input("Please input Token Decimals: "))

	recevier_num = eval(input("Please input recevier count: "))

	for _ in range(recevier_num):
		receiver_address = input("Please input recevier address(not with prefix 0x): ")
		amount = eval(input("Please input transfer amount: ")) * 10 ** token_decimals
		hex_amount = hex(amount)[2:].zfill(24)
		multi_transfer.append(receiver_address + hex_amount)

	result = "["
	for i in multi_transfer:
		result += i
		result += ","
	result += "\b]"

	print(result)

if __name__ == '__main__':
	main()