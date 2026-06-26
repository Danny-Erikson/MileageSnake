def build_service_card(file, services):
    data = []
    while len(services) != 0:
        data.append(services[0])
        # Here we checking if the current data and next date are the same,
        # if so continue until adding to data until we dont find a match
        if len(services) != 1 and services[0]["ServiceDate"] == services[1]["ServiceDate"]:
            services.pop(0)
            continue
        services.pop(0)
        # Once we are finshed with the start of the loop
        # Check if we have multiple services and write to the file accordingly
        if len(data) == 1:
            s = data[0]
            if s["ServiceId"] == None:
                card_type = "general"
            else:
                card_type = "reoccurring"
            file.write(f"""    <div class="card {card_type}">
      <div class="title">{s["Name"]}</div>
      <div class="flex-container">
        <div class="flex-item">Done At:<span class="smaller"> {s["ServiceMileage"]:,} miles</span></div>
        <div class="flex-item">Done on:<span class="smaller"> {s["ServiceDate"][5:]}-{s["ServiceDate"][:4]}</span></div>
      </div>
      <div class="notes">Notes:<span class="smaller">{s["Note"]}</span></div>
    </div>
""")
        else:
            file.write(f"""    <div class="card reoccurring">
      <div class="title">Multiple Services</div>
      <div class="flex-container">
        <div class="flex-item">Done At:<span class="smaller"> {data[0]["ServiceMileage"]:,} miles</span></div>
        <div class="flex-item">Done on:<span class="smaller"> {data[0]["ServiceDate"][5:]}-{data[0]["ServiceDate"][:4]}</span></div>
      </div>
""")
            for s in data:
                if s["ServiceId"] == None:
                    card_type = "general"
                else:
                    card_type = "reoccurring"
                file.write(f"""      <div class="card {card_type}">
        <div class="title">{s["Name"]}</div>
        <div class="notes">Notes:<span class="smaller">{s["Note"]}</span></div>
      </div>
""")
            file.write("""    </div>
""")
        data = []
