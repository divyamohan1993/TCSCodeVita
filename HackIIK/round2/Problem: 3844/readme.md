```markdown
# SQL Injection Analysis - SOC Engineer Task

## Problem Statement
As a SOC (Security Operations Center) engineer at a leading cybersecurity firm, you are tasked with analyzing a `.csv` file derived from a `.pcap` file to extract critical information about an **SQL injection attack**. The `.csv` file contains multiple protocols and application details.

### Input File Format (`input.csv`)
The file contains the following columns:
- **No.**: Packet number.
- **Time**: Packet capture timestamp.
- **Source**: Source IP address.
- **Destination**: Destination IP address.
- **Protocol**: Protocol used (e.g., HTTP).
- **Length**: Packet length.
- **Info**: Packet details.

---

## Task
Write a Python program to automate the extraction of insights related to the SQL injection attack. The output should include:

1. **Source IP Address**: The attacker's IP address (if any).  
   **Output Format**: `1A:-Source IP-;`  
   If no attacks are detected, output: `1A:-NULL-;`

2. **Count of SQL Injection Attempts**: Total number of SQL injection attempts made by the attacker.  
   **Output Format**: `2A:-Total SQL Injection Attempts-;`  
   If no attacks are detected, output: `2A:-0-;`

3. **Initial SQL Injection Attempt**: The URI of the first SQL injection attempt.  
   **Output Format**: `3A:-First Payload-;`  
   If no attempts are detected, output: `3A:-NULL-;`

4. **Final SQL Injection Attempt**: The URI of the last SQL injection attempt.  
   **Output Format**: `4A:-Last Payload-;`  
   If no attempts are detected, output: `4A:-NULL-;`

5. **Payloads Using Formatting Symbols**: Number of SQL injection attempts containing the formatting symbol (`:`).  
   **Output Format**: `5A:-Number of Payloads Containing formatting symbol-;`  
   If no such payloads are detected, output: `5A:-0-;`

---

## Output Format
The program should display results on separate lines, adhering strictly to the specified format:
```plaintext
1A:-value-;
2A:-value-;
3A:-value-;
4A:-value-;
5A:-value-;
```

---

## Example Input and Output

### Input
`file1.csv`  
Sample data (columns: No., Time, Source, Destination, Protocol, Length, Info):
```plaintext
No.,Time,Source,Destination,Protocol,Length,Info
1,0.001,10.0.2.5,192.168.0.1,HTTP,60,GET /dvwa/vulnerabilities/sqli/?id=2'&Submit=Submit HTTP/1.1
2,0.002,10.0.2.5,192.168.0.1,HTTP,80,GET /dvwa/vulnerabilities/sqli/?id=2'+union+select+group_concat(user_id,0x3a,user,0x3a,password),2+from+users--+&Submit=Submit HTTP/1.1
```

### Expected Output
```plaintext
1A:-10.0.2.5-;
2A:-20-;
3A:-/dvwa/vulnerabilities/sqli/?id=2'&Submit=Submit-;
4A:-/dvwa/vulnerabilities/sqli/?id=2'+union+select+group_concat(user_id,0x3a,user,0x3a,password),2+from+users--+&Submit=Submit-;
5A:-2-;
```

---

## Evaluation Criteria
- **Input Adaptability**: The program should work with any `.csv` file adhering to the described format.
- **Exact Output Format**: Follow the specified format closely to avoid point deductions.
- **Dynamic Processing**: Avoid hardcoding values; adapt to varying input.

---

## Notes
- **Sample .csv file**: Provided for development and testing.
- **Evaluation**: The program will be tested with five test cases:
  - **1 visible** test case.
  - **4 hidden** test cases.  
Each test case is worth **20 points**, with a total score of **100 points**.

```plaintext
# Test Case Results Example
INPUT            EXPECTED OUTPUT                                                                                                    ACTUAL OUTPUT
1 file1.csv      1A:-10.0.2.5-;                                                                                                    1A:-10.0.2.5-;
                 2A:-20-;                                                                                                         2A:-20-;
                 3A:-/dvwa/vulnerabilities/sqli/?id=2'&Submit=Submit-;                                                            3A:-/dvwa/vulnerabilities/sqli/?id=2'&Submit=Submit-;
                 4A:-/dvwa/vulnerabilities/sqli/?id=2'+union+select+group_concat(user_id,0x3a,user,0x3a,password),2+from+users--+&Submit=Submit-;
                 5A:-2-;                                                                                                         4A:-/dvwa/vulnerabilities/sqli/?id=2'+union+select+group_concat(user_id,0x3a,user,0x3a,password),2+from+users--+&Submit=Submit-;
                                                                                                                                5A:-2-;
```
```