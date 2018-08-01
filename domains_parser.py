import sys


def get_second_level_domains(result_lines, cert_domain_string):
    print "Get second level domain and/or wildcard SSL domain from certification"
    domains = cert_domain_string.split(",")

    tmp_domains = []

    for domain in domains:
        if "*" not in domain and "." in domain:
            domain_splitted = domain.split(".")
            if (domain_splitted[-2] != "com") and (domain_splitted[-2] != "org") and (domain_splitted[-2] != "net"):
                domain = domain_splitted[-2] + "." + domain_splitted[-1]
            else:
                domain = domain_splitted[-3] + "." + domain_splitted[-2] + "." +  domain_splitted[-1]

            print "Got second level domain: " + domain.replace("\n", "")

            tmp_domains.append( domain.replace("\n", "") )
        if "*" in domain:
            tmp_domains.append( domain.replace("\n", "").replace("*.", "").replace("*", "") )

    domains = list(tmp_domains)

    for domain in domains:
        result_lines.append(domain)

def get_domains(result_lines, cert_domain_string):
    print "Get all domains from certification"
    domains = cert_domain_string.split(",")

    tmp_domains = []

    for domain in domains:
        if "*" not in domain and "." in domain:
            print "Got domain: " + domain.replace("\n", "")
            tmp_domains.append( domain.replace("\n", "") )

    domains = list(tmp_domains)

    for domain in domains:
        result_lines.append(domain)


if len(sys.argv) < 4:
    print """A tool to get domains or company wildcard domain from result of sslScrape
Usage: python domain_parser.py [sslScrape_result_file] [work_id]
[work_id] 
    "1" - to parse all second level domains
    "2" - to get all domains in certificates

[result_file]
    Write the result to this file    
"""
    sys.exit(0)

with open(sys.argv[1], "r") as f:
    lines = f.readlines()

work_id = sys.argv[2] # - "1" to get second level domains, - "2" to get domains
result_file = sys.argv[3]

# the result of our work
result_lines = []

for line in lines:
    if ":" not in line:
        # not a result we need
        continue
    else:
        line_list = line.split(":")

        if line_list[1] == "failed\n":
            # sslScrape has faild on this host
            continue
        else:
            #print line_list[1]
            if work_id == "1":
                get_second_level_domains(result_lines, line_list[1])
            if work_id == "2":
                #print "Working with: " + line_list[1]
                get_domains(result_lines, line_list[1])

# make each item in result_lines to be unique
result_lines = list(set(result_lines))

with open(result_file, "w") as f:
    for line in result_lines:
        f.write(line + "\n")
            
