def build_title_card(file, car, text_color):
    file.write(f"""    <div class="card" style="background-color: {car["Color"]}; color: {text_color}">
      <h1>{car["Year"]} {car["Make"]} {car["Model"]}<span class="smaller">{car["Trim"] or ""}</span></h1>
      <div class="flex-container">
        <div class="flex-item">License Plate: <span class="smaller">{car["LicensePlate"]}</span></div>
        <div class="flex-item">VINNumber: <span class="smaller">{car["VINNumber"]}</span></div>
      </div>
    </div>
""")
