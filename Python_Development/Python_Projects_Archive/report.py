def main():
    spacecraft = {"Name": "Voyager 1", "Distance": "143"}
    print(create_report(spacecraft))
def create_report(spacecraft):
    return f"""
    ==========Report==========
    Name: {spacecraft['Name']}
    Distance: {spacecraft['Distance']} AU
    ==========================
    """

main()