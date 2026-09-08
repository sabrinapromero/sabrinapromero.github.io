import json, os, subprocess, sys, urllib.request

SEL = {
 "hornea": ["DXCumKCmHEF","DcouoxbsTx4","DXrqte8jpG_","DbskK_cjtkR","DZAHhxvAMWb",
            "DcdhCjBmw0L","DcJUBKAjv4R","DcEavAyMX9L","DbgFIhQuyJa","DcWF2R5DqRm"],
 "loyola": ["DYWzpM5A049","DZdphDhgMXU","DbMKwx6D8PG","DYE7GD8h3tY","Db6J0Dxp1Qg",
            "Db_j0z9p3am","DcV3O3Vhh40","DbD_ZciILLU","Dc3eNeXp6uH","Db6N5KNpt86"],
 "vincenzo": ["DXx7bmHjWBs","DWnQjEYj-p8","DcgXyTACiMx","DbtGhLvDr-B","DVm4lnnDWKw",
              "DcbLxvMDb0U","DaoKE5VmVNT","DURIJO0kuBV","DTSsH2vjaAc","DbYO8luOOHI"],
 "urano": ["DYkpdu2hPAR","DXx8BMfnAik","DS3HhUkgY4J","DTSshmvAHlx","DSGMDNigSGd"],
 "capsula": ["DM9AchXNRfm","DaZG2R2DeF2","DboV7BuGYgu","DbdiDzAEZGQ","Da0BAkSlqW4",
             "Daq4cYfmag6","Dct0IvuGdSJ","DbvfheqEbuI"],
 "boschi": ["DZvXkcimN3M","DU1npG8j7Z5","DYR4kUsDqD4","DbwMB7CmM46","DZlGgygmBQx"],
 "sabrina": ["DOSSeSDjA8Z","DX12mFwxppf","DGtxNP4xadv","DOzeQOpEbbW","DIUwn7RxtEg",
             "DQiT58TkbBm","DODzGc5EfiC"],
}

urls = {i["shortCode"]: i["displayUrl"]
        for i in json.load(open("data/ig_display_urls.json", encoding="utf-8"))["items"]}

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")

ok = fail = 0
for marca, codes in SEL.items():
    for c in codes:
        u = urls.get(c)
        if not u:
            print("SIN URL", marca, c); fail += 1; continue
        raw = f"assets/raw/{marca}_{c}.jpg"
        if os.path.exists(raw) and os.path.getsize(raw) > 5000:
            ok += 1; continue
        try:
            req = urllib.request.Request(u, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=45) as r, open(raw, "wb") as f:
                f.write(r.read())
            ok += 1
        except Exception as e:
            print("ERROR", marca, c, type(e).__name__, e); fail += 1

print(f"descargadas={ok} fallidas={fail}")
