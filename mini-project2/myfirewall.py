from socket import *


def firewall(packet, Rules, f2):
    recievedIP = packet.split()[0]
    recievedPort = packet.split()[2]
    recievedFlag = packet.split()[4]

    MyIPAddresses = []
    MyPorts = []
    MyActions = []

    listEstablished = []
    counter = 0

    for i in Rules:
        MyActions.append(i.split(",")[0])
        MyIPAddresses.append(i.split(",")[1])
        MyPorts.append(i.split(",")[2])

        if "established" in i:
            listEstablished.append(counter)

        counter += 1

    if recievedFlag == "Continue":
        for j in listEstablished:
            if MyIPAddresses[j] != "*":
                subnetMask = MyIPAddresses[j].split("/")[1]
                ip = MyIPAddresses[j].split("/")[0]

                if subnetMask == "32":
                    if ip == recievedIP:
                        if MyPorts[j] == "*" or MyPorts[j] == recievedPort:
                            f2.write(f'{packet}: {MyActions[j]}\n')
                            print(MyActions[j] + "\n")
                            break

                elif subnetMask == "24":
                    listrulesIP = MyIPAddresses[j].split("/")[0].split(".")
                    listrecievedIP = recievedIP.split(".")

                    lastIP = int(listrecievedIP[3])
                    lastIP2 = int(listrulesIP[3])

                    if (listrecievedIP[0] == listrulesIP[0]) and (listrecievedIP[1] == listrulesIP[1]) and (
                            listrecievedIP[2] == listrulesIP[2]) and ((lastIP >= lastIP2) and (lastIP <= 255)):
                        if MyPorts[j] == "*" or MyPorts[j] == recievedPort:
                            f2.write(f'{packet}: {MyActions[j]}\n')
                            print(MyActions[j] + "\n")
                            break

            else:
                if MyPorts[j] == "*" or MyPorts[j] == recievedPort:
                    f2.write(f'{packet}: {MyActions[j]}\n')
                    print(MyActions[j] + "\n")
                    break

            if j == listEstablished[len(listEstablished) - 1]:
                f2.write(f'{packet}: block\n')
                print("block\n")

    else:
        for j in range(len(MyIPAddresses)):
            if MyIPAddresses[j] != "*":
                subnetMask = MyIPAddresses[j].split("/")[1]
                ip = MyIPAddresses[j].split("/")[0]

                if subnetMask == "32":
                    if ip == recievedIP:
                        if MyPorts[j] == "*" or MyPorts[j] == recievedPort:
                            f2.write(f'{packet}: {MyActions[j]}\n')
                            print(MyActions[j] + "\n")
                            break

                elif subnetMask == "24":
                    listrulesIP = MyIPAddresses[j].split("/")[0].split(".")
                    listrecievedIP = recievedIP.split(".")

                    lastIP = int(listrecievedIP[3])
                    lastIP2 = int(listrulesIP[3])

                    if (listrecievedIP[0] == listrulesIP[0]) and (listrecievedIP[1] == listrulesIP[1]) and (
                            listrecievedIP[2] == listrulesIP[2]) and ((lastIP >= lastIP2) and (lastIP <= 255)):
                        if MyPorts[j] == "*" or MyPorts[j] == recievedPort:
                            f2.write(f'{packet}: {MyActions[j]}\n')
                            print(MyActions[j] + "\n")
                            break

            else:
                if MyPorts[j] == "*" or MyPorts[j] == recievedPort:
                    f2.write(f'{packet}: {MyActions[j]}\n')
                    print(MyActions[j] + "\n")
                    break

            if j == listEstablished[0] - 1:
                f2.write(f'{packet}: block\n')
                print("block\n")
                break

serverIP = "127.0.0.1"
serverPort = 6677

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((serverIP, serverPort))


file = open('Rules.txt', 'r')
file2 = open('Actions.txt', 'w')
file2.write('|srcIP|  |dstIP|  |srcPort|  |dstPort|  |Flag|  |Action|\n')
file2.close()
rules = file.readlines()

print("The server is ready to receive\n")

while 1:
    message, clientAddress = serverSocket.recvfrom(2048)
    file2 = open('Actions.txt', 'a')
    print(f"A connection was made with : {clientAddress}")
    print(message.decode("utf-8"))

    if message.decode("utf-8") == "End connection":
        file2.close()
        break

    firewall(message.decode("utf-8"), rules, file2)
    file2.close()
