import redis
import random
import string
import json

r = redis.StrictRedis(host='localhost', port=6379, db=0)
SESSION_DURATION = 30 * (60 * 60 * 24)

def registerUser(ssn, name, password, role):
    if r.hget('users', ssn):
        return False
    
    else:
        userData = {
            'name': name,
            'password': password,
            'role': role,
        }
        
        r.hset('users', ssn, json.dumps(userData))
        return True

def updateUser(ssn, data):
    userData = r.hget('users', ssn)

    if userData:
        userData = json.loads(userData)
        userData.update(data)

        r.hset('users', ssn, json.dumps(userData))
        return True
    
    return False

def getUser(ssn):
    userData = r.hget('users', ssn)

    if userData:
        userData = json.loads(userData)
        return userData
    
    return None

def login(ssn, password):
    userData = r.hget('users', ssn)
    
    if userData:
        userData = json.loads(userData)
        
        if userData['password'] == password:
            token = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
            r.setex(token, SESSION_DURATION, ssn)
           
            role = int(userData['role'])
            return {'token': token, 'role': role}
    
    return {'token': None, 'role': -1}

def loginWithToken(token):
    ssn = r.get(token)
    
    if ssn:
        r.expire(token, SESSION_DURATION)
        
        userData = json.loads(r.hget('users', ssn))
        
        role = int(userData['role'])
        return {'role': role}
    
    return {'role': -1}

def registerRequest(userId, priority):
    r.zadd('requests', {json.dumps({'user_id': userId, 'priority': priority}): priority})

def attendRequests(): 
    while True:
        request = r.bzpopmax('requests', timeout=0)

        if request:
            requestData = json.loads(request[1].decode())
            
            userId = requestData['user_id']
            priority = requestData['priority']
            print(f"Attending to user {userId} with priority {priority}")

def main():
    # Connect to Redis
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    
    # Users data (json format)
    users = [
        {"ssn": "459-12-6789", "name": "John Doe", "password": "John123", "role": 1},
        {"ssn": "321-45-9876", "name": "Jane Smith", "password": "JanePass", "role": 2},
        {"ssn": "654-32-1987", "name": "Carlos Ramirez", "password": "CarlosSecure", "role": 1},
        {"ssn": "789-01-2345", "name": "Linda Martinez", "password": "LindaStrong", "role": 3},
        {"ssn": "234-56-7890", "name": "Emily Johnson", "password": "Emily789", "role": 5}
    ]

    for user in users:
        registerUser(user["ssn"], user["name"], user["password"], user["role"])

    print("Registered user data:")
    for user in users:
        print(getUser(user["ssn"]))
    
    print("\n")
    
    # Perform test logins
    for user in users:
        loginRes = login(user["ssn"], user["password"])
        if loginRes["token"]:
            print(f"Successful login for {user['name']}. Role: {loginRes['role']}")
        else:
            print(f"Failed login for {user['name']}")

    print("\n")

    # Perform a test login with token
    registerUser("567-89-0123", "Michael Brown", "MikeSecure", 3)
    loginRes = login("567-89-0123", "MikeSecure")
    token = loginRes['token']

    loginTokenRes = loginWithToken(token)
    if loginTokenRes['role'] != -1:
        print(f"Login with token -> Role: {loginTokenRes['role']}")
    else:
        print("Error: Login with token")
    
    print("\n")

    # Update user data ({"ssn": "459-12-6789", "name": "John Doe", "password": "John123", "role": 1})
    newData = {"name": "Johnathan Doe", "role": 4}
    if updateUser("459-12-6789", newData):
        print(f"Updated data: {getUser('459-12-6789')}")

    print("\n")

    # Simulate help requests
    for user in users:
        registerRequest(user["ssn"], random.randint(1, 5))

    # Simulate attending to requests
    attendRequests()

if __name__ == '__main__':
    main()