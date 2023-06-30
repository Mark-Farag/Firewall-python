from socket import *
from random import randrange

clientSocket = socket(AF_INET, SOCK_DGRAM)


def packetHandler(sourceIP, sourcePort, flag):
    destinationIP = "127.0.0.1"
    destinationPort = 6677
    if flag == "End connection":
        packet = flag
    else:
        packet = sourceIP + " " + destinationIP + " " + sourcePort + " " + str(destinationPort) + " " + flag

    clientSocket.sendto(bytes(packet, "utf-8"), (destinationIP, destinationPort))


def IPGenerator():
    flags = [" Start ", " Continue ", " End "]
    firewallIPs = [["127.0.0.1/32", "80"], ["192.168.2.0/24", "*"], ["*", "25"], ["*", "21"], ["*", "*"]]

    for i in firewallIPs:
        newIP = ""
        pktsOfIps = randrange(1, 5)

        if i[1] == "*":
            port = str(randrange(1, 65535 + 1))
        else:
            port = i[1]

        if i[0] != '*':
            currentIP = i[0].split("/")[0]
            subnetMask = i[0].split("/")[1]

            if subnetMask == "32":
                newIP = currentIP

            elif subnetMask == "24":
                newIP = currentIP.split('.')[0] + '.' + currentIP.split('.')[1] + '.' + currentIP.split('.')[
                    2] + '.' + str(randrange(int(currentIP.split('.')[3]), 256))

            elif subnetMask == "16":
                newIP = currentIP.split('.')[0] + '.' + currentIP.split('.')[1] + '.' + str(randrange(int(currentIP.split('.')[2]), 256)) + '.' + str(randrange(int(currentIP.split('.')[3]), 256))
        else:
            newIP += str(randrange(1, 256))
            for j in range(3):
                newIP += '.'
                newIP += str(randrange(0, 256))

        for k in range(pktsOfIps):
            if k == 0:
                flag = flags[0]
            elif k == pktsOfIps - 1:
                flag = flags[2]
            else:
                flag = flags[1]

            packetHandler(newIP, port, flag)

    packetHandler("", "", "End connection")


if __name__ == "__main__":
    IPGenerator()
