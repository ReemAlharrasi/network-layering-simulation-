"""
COMP3502 - computer netwroks
Assignment 1

Group Members: 
    Zainab Al Maamari 131137
    Reem Al Harrasi 126146
    Wafa Al-Maashani 130690
"""

"""
Application class
"""
class Application:
    
    def __init__(self):
        pass
        
    def sendMsg(self): 
        #asking the user to enter his msg
        msg= input("Enter your message please: ")
        #print the alerting of user's sent msg
        print("Alert: message is being sent. . .\n\n")
        return msg 
    # function of recieving msg
    def recieveMsg(self,decryption,haserror):
       print("Alert:a message just got recieved!")#show alert
       if haserror:
           print("      unfortunately, the message got an error")
       print("The message is: ", decryption)   
       
"""
splitJoinCheckSum class
"""
class splitJoin:
    def __init__(self,input):
        self.message=input
        self.packets=input
       
    def splitmsg(self):
        #splitting msg into char
        lst=[]
        for char in self.message:
            lst.append(char)
        
        #storing each char into a apacket
        packets=[]
        packet=""
        checksum=0 #for checking value
        for i in range(len(lst)):
            packet+=lst[i] #adding bytes to packet
            checksum+=ord(lst[i])
            #when packet is full or we reached msg's ended
            if len(packet)==5 or i==len(lst)-1:
                while len(packet)<5:
                    packet+="0"
                checksum=checksum%256
                packet+=str(checksum)
                packets.append(packet)
                packet=""
                checksum=0
            
        print(packets,"\n\n")
        return packets
        
    def joinCheckSum(self):
        #initialize needed variables
        message=""
        oldchecksum=""
        newChecksum=0
        haserror=False #set boolean to indicate error if there is any
        packets=self.packets
        #gettiing packets from list
        for i in range(len(packets)):
            oldchecksum=""
            newChecksum=0
            packet=packets[i]
            #getting bytes in every packet
            for j in range(5):
                if i==len(packets)-1 and packet[j]=="0":
                    break
                message+=str(packet[j])
                newChecksum+=ord(packet[j])
            for h in range(5,len(packet)):
                oldchecksum+=packet[h]
            oldchecksum=int(oldchecksum)
            newChecksum=newChecksum%256
            #compare old and new checksum
            if oldchecksum!=newChecksum:
                haserror=True
        print(message)
        return message,haserror
"""
Encrypt & Decrypt class
"""
class encryptdecrypt:
    def __init__(self,input):  #Initializing the constructor
        self.packets=input
       
    def encrypt(self):
        lowerCase= 'abcdefghijklmnopqrstuvwxyz'      
        upperCase= 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        e_packets=[]#empty string
        for packet in self.packets:
            e_packet=""
            for char in packet:#for every charecter in the string
                if char.isalpha()and char.isupper():#The input must be a string 
                    #applaying ro13  if the string is in uppercase
                    i=(upperCase.index(char)+13)%26
                    #adding the encrypted letters to e_packets
                    e_packet+=upperCase[i]
                elif char.isalpha()and char.islower():
                    #applaying ro13  if the string is in lowercase
                    i=(lowerCase.index(char)+13)%26
                    e_packet+=lowerCase[i]
                else:
                    e_packet+=char
            e_packets.append(e_packet)
        print(e_packets,"\n\n")#print the encrypted version of the string
        return e_packets
    
    def decrypt(self):
        lowerCase= 'abcdefghijklmnopqrstuvwxyz'
        upperCase= 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        d_packets=[]
        for packet in self.packets:
            d_packet=""
            for char in packet:
                if char.isalpha()and char.isupper():
      #applaying the opposite of ro13 to decrypt if the string is in uppercase
                    i=(upperCase.index(char)-13)%26
                    #adding the decrypted letters to e_packets
                    d_packet+=upperCase[i]             
                elif char.isalpha()and char.islower(): 
      #applaying the opposite of ro13 to decrypt if the string is in lowercase
                    i=(lowerCase.index(char)-13)%26
                    #adding the decrypted letters to e_packets
                    d_packet+=lowerCase[i]
                else:
                    d_packet+=char
            d_packets.append(d_packet)
        print(d_packets,"\n\n")#print the decrypted version of the string
        return d_packets
"""
Physical class
"""
import random

class physical:
    def __init__(self,packets):
        self.packets = packets
        
    def error(self):
        ERROR_PROBABILITY=0.5
        rand_prob = random.uniform(0, 1) #random probability
        randomAlpha= 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        chngindex=random.randint(0,50) #new char
        if rand_prob > ERROR_PROBABILITY:
            #find position to have an error on it
            packetIndex=random.randint(0, len(self.packets)-1)
            charIndex=random.randint(0,4)
        # errorpacket=self.packets[packetIndex] #split packet into char in list
            errorpacket=list(map(str,self.packets[packetIndex]))
            #in case the new char is the same as the old one
            if randomAlpha[chngindex].islower()== \
                errorpacket[charIndex].islower():
                chngindex-=1
            errorpacket[charIndex]=randomAlpha[chngindex]
            #change error packet to string
            self.packets[packetIndex]=''.join(errorpacket)
        print(self.packets,"\n\n")
        return self.packets
               
"""
main class
"""    
class main:
    def __init__(self):
        pass
    def start(self):
        ####create applications and send message
        print("-"*65)
        print(' '*22,"APPLICATION 1 LAYER")
        print("-"*65)
        app1=Application()
        app2=Application()
        msg=app1.sendMsg() 
        
        ####split message
        print("-"*65)
        print(" "*22, "SPLIT LAYER")
        print("-"*65)
        print("splitting message into packets. . .")
        print("packets:")
        splitmsg=splitJoin(msg)
        packets=splitmsg.splitmsg()
        ####encrypt
        print("-"*65)
        print(" "*22, "ENCRYPT LAYER") 
        print("-"*65)
        print("encrypting packets. . .")
        print("encrypted packets:")
        encryptmsg=encryptdecrypt(packets)
        encryptedmsg=encryptmsg.encrypt()

        ####physical
        print("-"*65)
        print(" "*22, "PHYSICAL LAYER")
        print("-"*65)
        print("signaling message to the other end. . .")
        print("this process is error-prone. . .")
        physicalprocess=physical(encryptedmsg)
        physicaldone=physicalprocess.error()
        print()

        ####decrypt
        print("-"*65)
        print(" "*22, "DECRYPT LAYER") 
        print("-"*65)
        print("decrypting packets. . .")
        print("decrypted packets:")
        decryptmsg=encryptdecrypt(physicaldone)
        decryptedmsg=decryptmsg.encrypt()

        ####join&checksum
        print("-"*65)
        print(" "*22, "JOIN & CHECKSUM LAYER") 
        print("-"*65)
        print("joining packets to extract the message. . .")
        print("joined message:")
        joinedmsg=splitJoin(decryptedmsg)
        newmsg,haserror=joinedmsg.joinCheckSum()
        
        ####recieve
        print("-"*65)
        print(" "*22, "APPLICATION 2 LAYER") 
        print("-"*65)
        app2.recieveMsg(newmsg,haserror)
     
main=main()
main.start()



