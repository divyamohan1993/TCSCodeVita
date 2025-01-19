import hashlib

def compute_merkle_root(transactions):
    if len(transactions) == 1:
        return hashlib.sha256(transactions[0].encode()).hexdigest()
    
    current_level = transactions[:]
    
    while len(current_level) > 1:
        if len(current_level) % 2 != 0:
            current_level.append(current_level[-1])
        
        new_level = []
        
        for i in range(0, len(current_level), 2):
            pair_concat = current_level[i] + current_level[i+1]
            pair_hash = hashlib.sha256(pair_concat.encode()).hexdigest()
            new_level.append(pair_hash)
        
        current_level = new_level
    
    return current_level[0]


def main():
    T = int(input().strip())
    
    for _ in range(T):
        N = int(input().strip())
        
        transactions = [input().strip() for _ in range(N)]
        
        merkle_root = compute_merkle_root(transactions)
        
        print(merkle_root)

if __name__ == "__main__":
    main()
