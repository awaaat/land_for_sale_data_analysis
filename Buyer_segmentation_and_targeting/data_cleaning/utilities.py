class Utilities:
    def __init__(self):
        self.kenyan_counties = {
        "Mombasa": ["Mombasa", "Mvita", "Saba Saba", "Majengo", "Changamwe", "Jomvu", "Kisauni", "Likoni", "Nyali", "Bamburi", "Kongowea", "Tudor", "Mtwapa", "Shanzu", "Frere Town", "Mkomani", "Kizingo", "Tononoka", "Magongo", "Mikindani"],
        "Kwale": ["Kwale", "Kinango", "Lunga Lunga", "Msambweni", "Ukunda", "Diani", "Mazeras", "Shimoni", "Tiwi", "Matuga", "Gombato", "Ng'ombeni", "Mkongani", "Ramisi"],
        "Kilifi": ["Kilifi", "Ganze", "Kaloleni", "Mtwapa", "Magarini", "Malindi", "Rabai", "Watamu", "Mariakani", "Kaloleni Town", "Vipingo", "Mavueni", "Gongoni", "Bamba", "Chasimba", "Tezo"],
        "Tana River": ["Hola", "Bura", "Garsen", "Madogo", "Banga", "Minjila", "Ngao", "Kipini"],
        "Lamu": ["Lamu", "Faza", "Mpeketoni", "Witu", "Mokowe", "Hindi", "Siyu"],
        "Taita Taveta": ["Voi", "Mwatate", "Taveta", "Wundanyi", "Maungu", "Bura Station", "Mghange", "Tsavo", "Mackinnon Road"],
        "Garissa": ["Garissa", "Dadaab", "Fafi", "Hulugho", "Ijara", "Modogashe", "Balambala", "Masalani", "Bura East", "Shant-Abak", "Nanighi"],
        "Wajir": ["Wajir", "Eldas", "Tarbaj", "Bute", "Habaswein", "Griftu", "Buna", "Diff", "Wajir-Bor", "Gurard"],
        "Mandera": ["Mandera", "Banissa", "Lafey", "Rhamu", "Elwak", "Takaba", "Mandera East", "Kutulo", "Fino"],
        "Marsabit": ["Marsabit", "Laisamis", "Moyale", "North Horr", "Sololo", "Kalacha", "Illeret", "Dukana"],
        "Isiolo": ["Isiolo", "Merti", "Garbatulla", "Oldonyiro", "Kinna", "Sericho"],
        "Meru": ["Meru", "Timau", "Maua", "Laare", "Nkubu", "Mitunguu", "Muriri", "Kianjai", "Githongo", "Igoji", "Kanyakine", "Mikinduri", "Gatimbi"],
        "Tharaka Nithi": ["Chuka", "Marimanti", "Chogoria",
                        "Maara", "Chiakariga", "Muthambi", "Kathwana", "Magutuni", "Kibirichia",
                        "Karingani", "Gatunga"],
        "Embu": ["Embu", "Siakago", "Kiritiri", "Runyenjes", "Manyatta", "Kithimu", "Mwea", "Ishianga"],
        "Kitui": ["Kitui", "Kakeani", "Mwingi", "Mutomo", "Kyuso", "Migwani", "Mutitu", "Katulani", "Kisasi", "Nzambani", "Ikutha"],
        "Machakos": ["Machakos", "Kamulu", "Joska", "Malaa" , "Mavoko", "Muthwani", "Kathiani", "Mitaboni", "Mlolongo", "Masinga", "Ekalakala", "Tala", "Matungulu", "Athi River", "Kinanie", "DayStar Area", "Lukenya", "Syokimau", "Mwala", "Masii", "Kithimani", "Matuu", "Kangundo", "Kivaa", "Yatta"],
        "Makueni": ["Wote", "Kilala", "Kibwezi", "Mtito Andei", "Sultan Hamud", "Emali", "Makindu", "Kikima", "Kalawa", "Kasikeu", "Mukuyuni", "Mbitini", "Nguu/Masumba", "Mukaa", "Kathonzweni", "Nzaui/Kilili/Kalamba", "Kiima Kiu/Kalanzoni", "Kikumbulyu North", "Kilungu"],
        "Nyandarua": ["Ol Kalou", "Engineer", "Kipipiri", "Ndaragwa", "Ol Joro Orok", "Mairo-Inya", "Nyahururu", "Kinangop", "Mirangine", "Rurii", "Magumu", "Leshau Pondo", "Gatimu", "Murungaru", "NjabiniKiburu", "Karau", "Wanjohi", "Shamata", "Charagita", "Githabai", "Nyakio", "Weru", "Kiriita", "Gathanji"],
        "Nyeri": ["Nyeri", "Kieni", "Gakawa", "Gatarakwa", "Endarasha", "Mwiyogo", "Mugunda", "Mathira", "Magutu", "Naro Moru", "Mweiga", "Karatina", "Mukurweini", "Othaya", "Wamagana", "Ruringu", "Tetu", "Kiganjo", "Chinga"],
        "Kirinyaga": ["Kerugoya", "Kutus", "Kianyaga", "Baricho", "Kandongu", "Ngurubani", "Wanguru", "Sagana", "Kagio", "Kiamaciri", "Nyangati", "Murinduko", "Kiine", "Baragwi", "Mutithi", "Mutira", "Inoi", "Gathigiriri", "Kariti", "Njukiini", "Mukure", "Wamumu"],
        "Murang’a": ["Murang’a", "Gatanga", "Kahuro", "Kandara", "Kangema", "Kigumo", "Kenol", "Kiria-ini", "Maragua", "Makuyu", "Gacharage", "Kimorori/Wempa", "Kambiti", "Kamahuha", "Kakuzi/Mitubiri", "Nginda", "Gitugi", "Kagundu-Ini", "Mugumo-Ini", "Township G", "Ichagaki", "Rwathia", "Mbiri", "Muruka", "Mugoiri", "Ithanga"],
        "Kiambu": ["Lari", "Kinale", "Nyanduma", "Lari/Kirenga", "Kiambu", "Kamwangi", "Gatundu", "Ndarugu", "Githunguri", "Juja", "Witethie", "Kabete", "Kiambaa", "Karuri", "Ndenderu", "Thindigua", "Ruaka", "Kikuyu", "Limuru", "Ruiru", "Kimbo", "Kwa Kairu", "Thika", "Gachie", "Banana", "Tigoni", "Ndumberi", "Kinoo", "Wangige"],
        "Turkana": ["Lodwar", "Lorugum", "Lokori", "Lokitaung", "Kakuma", "Lokichar", "Kainuk", "Kalokol", "Kerio", "Kanamkemer"],
        "West Pokot": ["Kapenguria", "Sigor", "Kacheliba", "Makutano", "Chepareria", "Ortum", "Kapsowar"],
        "Samburu": ["Maralal", "Wamba", "Baragoi", "Archer’s Post", "Suguta Marmar", "Loruko"],
        "Trans Nzoia": ["Kitale", "Cherangany", "Endebess", "Kiminini", "Kwanza", "Saboti", "Kapsara", "Sitatunga", "Bidii"],
        "Uasin Gishu": ["Eldoret", "Ainabkoi", "Kapseret", "Kesses", "Moiben", "Soy", "Moi’s Bridge", "Turbo", "Ziwa", "Kaptagat", "Chepkoilel"],
        "Elgeyo Marakwet": ["Iten", "Chepkorio", "Kapsowar", "Kaptarakwa", "Cheptongei", "Kapsabet", "Kamariny"],
        "Nandi": ["Kapsabet", "Kobujoi", "Chemelil", "Kabiyet", "Nandi Hills", "Tindiret", "Mosoriot", "Kaiboi", "Kapkangani", "Ol'Lessos"],
        "Baringo": ["Kabarnet", "Kipsaraman", "Marigat", "Eldama Ravine", "Mogotio", "Chemolingot", "Kabartonjo", "Barwessa", "Churo/Amaya", "Ravine"],
        "Laikipia": [ "Laikipia West", "Thome", "Mutara", "Ndurumo", "Sipili", "Sosian", "Lonyiek","Laikipia Central", "Ngobit", "Nyambogishi", "Wiyumiririe", "Tigithi", "Laikipia East", "Muramati", "Segera", "Umande", "Nturukuma","Rumuruti", "Nanyuki", "Doldol", "Nyahururu", "Rumuruti Town", "Kinamba", "Lamuria", "Laikipia Central", "Laikipia East", "Laikipia North", "Ngobit", "Wiyumiririe", "Tigithi", "Githiga (Laikipia)"],
        "Nakuru": ["Nakuru", "Kuresoi North", "Kamara", "Dundori", "Gilgil", "Elementaita", "Eburru", "Mau Summit", "Keringet", "Molo", "Turi", "Elburgon", "Naivasha", "Mai Mahiu", "Njoro", "Rongai", "Subukia", "Salgaa", "Mau Narok", "Bahati", "Lanet"],
        "Narok": ["Narok", "Ololulunga", "Lemelepo", "Emurua Dikirr", "Kilgoris", "Suswa", "Nairegie Enkare", "Mulot"],
        "Kajiado": ["Kajiado", "Isinya", "Ngong", "Ol Keri", "Kiserian", "Loitokitok", "Mashuru", "Kitengela", "Namanga", "Ongata Rongai", "Magadi", "Oloolaimutia", "Bissil"],
        "Kericho": ["Kericho", "Sosiot", "Litein", "Kipkelion", "Fort Ternan", "Sigowet", "Londiani", "Chepseon", "Kapsuser"],
        "Bomet": ["Bomet", "Longisa", "Sigor", "Mogogosiek", "Sotik", "Chebole", "Silibwet", "Kaplong"],
        "Kakamega": ["Kakamega", "Butere", "Shinyalu", "Malava", "Ikolomani", "Khwisero", "Lugari", "Lukuyani", "Matete", "Mumias", "Mutungu", "Navakholo", "Shikoti", "Lumakanda", "Matungu"],
        "Vihiga": ["Vihiga", "Emuhaya", "Hamisi", "Luanda", "Sabatia", "Mbale", "Chavakali", "Serem", "Kaimosi"],
        "Bungoma": ["Bungoma", "Bumula", "Kabuchai", "Kimilili", "Kapsokwony", "Sirisia", "Tongaren", "Webuye", "Matete", "Chwele", "Kanduyi", "Naitiri"],
        "Busia": ["Busia", "Port Victoria", "Butula", "Funyula", "Nambale", "Amagoro", "Malaba", "Amukura", "Budalangi", "Matayos"],
        "Siaya": ["Siaya", "Bondo", "Yala", "Aram", "Ukwala", "Ugunja", "Nyilima", "Rarieda", "Ng’iya"],
        "Kisumu": ["Kisumu", "Seme", "Ratta", "Kolunje", "East Seme", "Kajulu", "Ojola", "Muhoroni", "Pap Onditi", "Central Nyakach", "Awasi", "Kombewa", "Maseno", "Ahero", "Katito", "Chemelil"],
        "Homa Bay": ["Homa Bay", "Kabondo", "Kendu Bay", "Oyugis", "Mbita", "Ndhiwa", "Rangwe", "Sindo", "Suba", "Rusinga"],
        "Migori": ["Migori", "Awendo", "Kegonga", "Kehancha", "Mabera", "Ntimaru", "Rongo", "Suna", "Uriri", "Isebania", "Macalder", "Kuria"],
        "Kisii": ["Kisii", "Kitutu Chache South", "Bogusero", "Nyamache", "Bonchari", "Riana", "Kenyenya", "Ogembo", "Marani", "Masaba", "Nyamarambe", "Suneka", "Kenyenya", "Gesusu", "Keroka"],
        "Nyamira": ["Nyamira", "Borabu", "Manga", "Keroka", "Ekerenyo", "Nyansiongo", "Ikonge"],
        "Nairobi": ["Langata", "Ngei Estate", "Deliverance","Dagoretti", "Waithaka", "Uthiru", "Kabiria", "Ruthimitu", "Mutuini", "Ngando", "Market Dagoretti", "Satelitte", "Dagoretti Corner""Jamhuri", "Woodley Estate", "Jamhuri Estate", "Nairobi", "Kariobangi", "Kariobangi South", "Kawangware", "Kilimani", "Ng’ando", "Riruta", "Kayole", "Komarock", "Mihango", "Utawala", "Dandora", "Imara Daima", "Kwa Njenga", "Umoja", "Mowlem", "Kamukunji", "Eastleigh", "Kasarani", "Githurai", "Kahawa", "Kibera", "Laini Saba", "Lang’ata", "Karen", "Makadara", "Viwandani", "Mathare", "Huruma", "Roysambu", "Zimmerman", "Kahawa West", "Ruaraka", "Baba Dogo", "Starehe", "Nairobi Central", "Pangani", "Westlands", "Parklands", "Kitisuru", "Kangemi", "South C", "Lavington", "Kileleshwa", "Donholm", "Embakasi", "Pipeline", "Buruburu", "London", "Section 58", "Piave Gardens", "Upperhill", "Milimani"],
        }
        
        self.population_parameters = {
            "MOMBASA": {
                "Total": 1208333,
                "Sex": {
                    "Male": 610257,
                    "Female": 598046,
                    "Intersex": 30
                },
                "Households": {
                    "Total": 378422,
                    "Conventional": 376295,
                    "Group quarters": 2127
                },
                "Land Area (Sq Km)": 220,
                "Density (Persons per Sq. Km)": 5495
            },
            "KWALE": {
                "Total": 866820,
                "Sex": {
                    "Male": 425121,
                    "Female": 441681,
                    "Intersex": 18
                },
                "Households": {
                    "Total": 173176,
                    "Conventional": 172802,
                    "Group quarters": 374
                },
                "Land Area (Sq Km)": 8254,
                "Density (Persons per Sq. Km)": 105
            },
            "KILIFI": {
                "Total": 1453787,
                "Sex": {
                    "Male": 704089,
                    "Female": 749673,
                    "Intersex": 25
                },
                "Households": {
                    "Total": 298472,
                    "Conventional": 297990,
                    "Group quarters": 482
                },
                "Land Area (Sq Km)": 12553,
                "Density (Persons per Sq. Km)": 116
            },
            "TANA RIVER": {
                "Total": 315943,
                "Sex": {
                    "Male": 158550,
                    "Female": 157391,
                    "Intersex": 2
                },
                "Households": {
                    "Total": 68242,
                    "Conventional": 66984,
                    "Group quarters": 1258
                },
                "Land Area (Sq Km)": 37904,
                "Density (Persons per Sq. Km)": 8
            },
            "LAMU": {
                "Total": 143920,
                "Sex": {
                    "Male": 76103,
                    "Female": 67813,
                    "Intersex": 4
                },
                "Households": {
                    "Total": 37963,
                    "Conventional": 34231,
                    "Group quarters": 3732
                },
                "Land Area (Sq Km)": 6283,
                "Density (Persons per Sq. Km)": 23
            },
            "TAITA TAVETA": {
                "Total": 340671,
                "Sex": {
                    "Male": 173337,
                    "Female": 167327,
                    "Intersex": 7
                },
                "Households": {
                    "Total": 96429,
                    "Conventional": 94468,
                    "Group quarters": 1961
                },
                "Land Area (Sq Km)": 17152,
                "Density (Persons per Sq. Km)": 20
            },
            "GARISSA": {
                "Total": 841353,
                "Sex": {
                    "Male": 458975,
                    "Female": 382344,
                    "Intersex": 34
                },
                "Households": {
                    "Total": 141394,
                    "Conventional": 138940,
                    "Group quarters": 2454
                },
                "Land Area (Sq Km)": 44753,
                "Density (Persons per Sq. Km)": 19
            },
            "WAJIR": {
                "Total": 781263,
                "Sex": {
                    "Male": 415374,
                    "Female": 365840,
                    "Intersex": 49
                },
                "Households": {
                    "Total": 127932,
                    "Conventional": 126878,
                    "Group quarters": 1054
                },
                "Land Area (Sq Km)": 56774,
                "Density (Persons per Sq. Km)": 14
            },
            "MANDERA": {
                "Total": 867457,
                "Sex": {
                    "Male": 434976,
                    "Female": 432444,
                    "Intersex": 37
                },
                "Households": {
                    "Total": 125763,
                    "Conventional": 123954,
                    "Group quarters": 1809
                },
                "Land Area (Sq Km)": 25942,
                "Density (Persons per Sq. Km)": 33
            },
            "MARSABIT": {
                "Total": 459785,
                "Sex": {
                    "Male": 243548,
                    "Female": 216219,
                    "Intersex": 18
                },
                "Households": {
                    "Total": 77495,
                    "Conventional": 76689,
                    "Group quarters": 806
                },
                "Land Area (Sq Km)": 70944,
                "Density (Persons per Sq. Km)": 6
            },
            "ISIOLO": {
                "Total": 268002,
                "Sex": {
                    "Male": 139510,
                    "Female": 128483,
                    "Intersex": 9
                },
                "Households": {
                    "Total": 58072,
                    "Conventional": 53217,
                    "Group quarters": 4855
                },
                "Land Area (Sq Km)": 25349,
                "Density (Persons per Sq. Km)": 11
            },
            "MERU": {
                "Total": 1545714,
                "Sex": {
                    "Male": 767698,
                    "Female": 777975,
                    "Intersex": 41
                },
                "Households": {
                    "Total": 426360,
                    "Conventional": 423931,
                    "Group quarters": 2429
                },
                "Land Area (Sq Km)": 7014,
                "Density (Persons per Sq. Km)": 220
            },
            "THARAKA NITHI": {
                "Total": 393177,
                "Sex": {
                    "Male": 193764,
                    "Female": 199406,
                    "Intersex": 7
                },
                "Households": {
                    "Total": 109860,
                    "Conventional": 109450,
                    "Group quarters": 410
                },
                "Land Area (Sq Km)": 2564,
                "Density (Persons per Sq. Km)": 153
            },
            "EMBU": {
                "Total": 608599,
                "Sex": {
                    "Male": 304208,
                    "Female": 304367,
                    "Intersex": 24
                },
                "Households": {
                    "Total": 182743,
                    "Conventional": 182427,
                    "Group quarters": 316
                },
                "Land Area (Sq Km)": 2821,
                "Density (Persons per Sq. Km)": 216
            },
            "KITUI": {
                "Total": 1136187,
                "Sex": {
                    "Male": 549003,
                    "Female": 587151,
                    "Intersex": 33
                },
                "Households": {
                    "Total": 262942,
                    "Conventional": 261814,
                    "Group quarters": 1128
                },
                "Land Area (Sq Km)": 30430,
                "Density (Persons per Sq. Km)": 37
            },
            "MACHAKOS": {
                "Total": 1421932,
                "Sex": {
                    "Male": 710707,
                    "Female": 711191,
                    "Intersex": 34
                },
                "Households": {
                    "Total": 402466,
                    "Conventional": 399523,
                    "Group quarters": 2943
                },
                "Land Area (Sq Km)": 6037,
                "Density (Persons per Sq. Km)": 236
            },
            "MAKUENI": {
                "Total": 987653,
                "Sex": {
                    "Male": 489691,
                    "Female": 497942,
                    "Intersex": 20
                },
                "Households": {
                    "Total": 244669,
                    "Conventional": 243979,
                    "Group quarters": 690
                },
                "Land Area (Sq Km)": 8177,
                "Density (Persons per Sq. Km)": 121
            },
            "NYANDARUA": {
                "Total": 638289,
                "Sex": {
                    "Male": 315022,
                    "Female": 323247,
                    "Intersex": 20
                },
                "Households": {
                    "Total": 179686,
                    "Conventional": 178224,
                    "Group quarters": 1462
                },
                "Land Area (Sq Km)": 3286,
                "Density (Persons per Sq. Km)": 194
            },
            "NYERI": {
                "Total": 759164,
                "Sex": {
                    "Male": 374288,
                    "Female": 384845,
                    "Intersex": 31
                },
                "Households": {
                    "Total": 248050,
                    "Conventional": 244564,
                    "Group quarters": 3486
                },
                "Land Area (Sq Km)": 3325,
                "Density (Persons per Sq. Km)": 228
            },
            "KIRINYAGA": {
                "Total": 610411,
                "Sex": {
                    "Male": 302011,
                    "Female": 308369,
                    "Intersex": 31
                },
                "Households": {
                    "Total": 204188,
                    "Conventional": 203576,
                    "Group quarters": 612
                },
                "Land Area (Sq Km)": 1478,
                "Density (Persons per Sq. Km)": 413
            },
            "MURANG’A": {
                "Total": 1056640,
                "Sex": {
                    "Male": 523940,
                    "Female": 532669,
                    "Intersex": 31
                },
                "Households": {
                    "Total": 318105,
                    "Conventional": 317496,
                    "Group quarters": 609
                },
                "Land Area (Sq Km)": 2523,
                "Density (Persons per Sq. Km)": 419
            },
            "KIAMBU": {
                "Total": 2417735,
                "Sex": {
                    "Male": 1187146,
                    "Female": 1230454,
                    "Intersex": 135
                },
                "Households": {
                    "Total": 795241,
                    "Conventional": 792333,
                    "Group quarters": 2908
                },
                "Land Area (Sq Km)": 2539,
                "Density (Persons per Sq. Km)": 952
            },
            "TURKANA": {
                "Total": 926976,
                "Sex": {
                    "Male": 478087,
                    "Female": 448868,
                    "Intersex": 21
                },
                "Households": {
                    "Total": 164519,
                    "Conventional": 162627,
                    "Group quarters": 1892
                },
                "Land Area (Sq Km)": 68233,
                "Density (Persons per Sq. Km)": 14
            },
            "WEST POKOT": {
                "Total": 621241,
                "Sex": {
                    "Male": 307013,
                    "Female": 314213,
                    "Intersex": 15
                },
                "Households": {
                    "Total": 116182,
                    "Conventional": 115761,
                    "Group quarters": 421
                },
                "Land Area (Sq Km)": 9123,
                "Density (Persons per Sq. Km)": 68
            },
            "SAMBURU": {
                "Total": 310327,
                "Sex": {
                    "Male": 156774,
                    "Female": 153546,
                    "Intersex": 7
                },
                "Households": {
                    "Total": 65910,
                    "Conventional": 63951,
                    "Group quarters": 1959
                },
                "Land Area (Sq Km)": 21090,
                "Density (Persons per Sq. Km)": 15
            },
            "TRANS NZOIA": {
                "Total": 990341,
                "Sex": {
                    "Male": 489107,
                    "Female": 501206,
                    "Intersex": 28
                },
                "Households": {
                    "Total": 223808,
                    "Conventional": 222989,
                    "Group quarters": 819
                },
                "Land Area (Sq Km)": 2495,
                "Density (Persons per Sq. Km)": 397
            },
            "UASIN GISHU": {
                "Total": 1163186,
                "Sex": {
                    "Male": 580269,
                    "Female": 582889,
                    "Intersex": 28
                },
                "Households": {
                    "Total": 304943,
                    "Conventional": 301110,
                    "Group quarters": 3833
                },
                "Land Area (Sq Km)": 3399,
                "Density (Persons per Sq. Km)": 342
            },
            "ELGEYO MARAKWET": {
                "Total": 454480,
                "Sex": {
                    "Male": 227317,
                    "Female": 227151,
                    "Intersex": 12
                },
                "Households": {
                    "Total": 99861,
                    "Conventional": 99119,
                    "Group quarters": 742
                },
                "Land Area (Sq Km)": 3032,
                "Density (Persons per Sq. Km)": 150
            },
            "NANDI": {
                "Total": 885711,
                "Sex": {
                    "Male": 441259,
                    "Female": 444430,
                    "Intersex": 22
                },
                "Households": {
                    "Total": 199426,
                    "Conventional": 199040,
                    "Group quarters": 386
                },
                "Land Area (Sq Km)": 2849,
                "Density (Persons per Sq. Km)": 311
            },
            "BARINGO": {
                "Total": 666763,
                "Sex": {
                    "Male": 336322,
                    "Female": 330428,
                    "Intersex": 13
                },
                "Households": {
                    "Total": 142518,
                    "Conventional": 141877,
                    "Group quarters": 641
                },
                "Land Area (Sq Km)": 10985,
                "Density (Persons per Sq. Km)": 61
            },
            "LAIKIPIA": {
                "Total": 518560,
                "Sex": {
                    "Male": 259440,
                    "Female": 259102,
                    "Intersex": 18
                },
                "Households": {
                    "Total": 149271,
                    "Conventional": 145776,
                    "Group quarters": 3495
                },
                "Land Area (Sq Km)": 9508,
                "Density (Persons per Sq. Km)": 55
            },
            "NAKURU": {
                "Total": 2162202,
                "Sex": {
                    "Male": 1077272,
                    "Female": 1084835,
                    "Intersex": 95
                },
                "Households": {
                    "Total": 616046,
                    "Conventional": 598237,
                    "Group quarters": 17809
                },
                "Land Area (Sq Km)": 7505,
                "Density (Persons per Sq. Km)": 288
            },
            "NAROK": {
                "Total": 1157873,
                "Sex": {
                    "Male": 579042,
                    "Female": 578805,
                    "Intersex": 26
                },
                "Households": {
                    "Total": 241125,
                    "Conventional": 238115,
                    "Group quarters": 3010
                },
                "Land Area (Sq Km)": 17932,
                "Density (Persons per Sq. Km)": 65
            },
            "KAJIADO": {
                "Total": 1117840,
                "Sex": {
                    "Male": 557098,
                    "Female": 560704,
                    "Intersex": 38
                },
                "Households": {
                    "Total": 316179,
                    "Conventional": 313218,
                    "Group quarters": 2961
                },
                "Land Area (Sq Km)": 21871,
                "Density (Persons per Sq. Km)": 51
            },
            "KERICHO": {
                "Total": 901777,
                "Sex": {
                    "Male": 450741,
                    "Female": 451008,
                    "Intersex": 28
                },
                "Households": {
                    "Total": 206036,
                    "Conventional": 205932,
                    "Group quarters": 104
                },
                "Land Area (Sq Km)": 2436,
                "Density (Persons per Sq. Km)": 370
            },
            "BOMET": {
                "Total": 875689,
                "Sex": {
                    "Male": 434287,
                    "Female": 441379,
                    "Intersex": 23
                },
                "Households": {
                    "Total": 187641,
                    "Conventional": 187230,
                    "Group quarters": 411
                },
                "Land Area (Sq Km)": 2507,
                "Density (Persons per Sq. Km)": 349
            },
            "KAKAMEGA": {
                "Total": 1867579,
                "Sex": {
                    "Male": 897133,
                    "Female": 970406,
                    "Intersex": 40
                },
                "Households": {
                    "Total": 433207,
                    "Conventional": 432284,
                    "Group quarters": 923
                },
                "Land Area (Sq Km)": 3017,
                "Density (Persons per Sq. Km)": 619
            },
            "VIHIGA": {
                "Total": 590013,
                "Sex": {
                    "Male": 283678,
                    "Female": 306323,
                    "Intersex": 12
                },
                "Households": {
                    "Total": 143365,
                    "Conventional": 143288,
                    "Group quarters": 77
                },
                "Land Area (Sq Km)": 564,
                "Density (Persons per Sq. Km)": 1047
            },
            "BUNGOMA": {
                "Total": 1670570,
                "Sex": {
                    "Male": 812146,
                    "Female": 858389,
                    "Intersex": 35
                },
                "Households": {
                    "Total": 358796,
                    "Conventional": 357714,
                    "Group quarters": 1082
                },
                "Land Area (Sq Km)": 3024,
                "Density (Persons per Sq. Km)": 552
            },
            "BUSIA": {
                "Total": 893681,
                "Sex": {
                    "Male": 426252,
                    "Female": 467401,
                    "Intersex": 28
                },
                "Households": {
                    "Total": 198152,
                    "Conventional": 197944,
                    "Group quarters": 208
                },
                "Land Area (Sq Km)": 1700,
                "Density (Persons per Sq. Km)": 526
            },
            "SIAYA": {
                "Total": 993183,
                "Sex": {
                    "Male": 471669,
                    "Female": 521496,
                    "Intersex": 18
                },
                "Households": {
                    "Total": 250698,
                    "Conventional": 249341,
                    "Group quarters": 1357
                },
                "Land Area (Sq Km)": 2530,
                "Density (Persons per Sq. Km)": 393
            },
            "KISUMU": {
                "Total": 1155574,
                "Sex": {
                    "Male": 560942,
                    "Female": 594609,
                    "Intersex": 23
                },
                "Households": {
                    "Total": 300745,
                    "Conventional": 296846,
                    "Group quarters": 3899
                },
                "Land Area (Sq Km)": 2085,
                "Density (Persons per Sq. Km)": 554
            },
            "HOMA BAY": {
                "Total": 1131950,
                "Sex": {
                    "Male": 539560,
                    "Female": 592367,
                    "Intersex": 23
                },
                "Households": {
                    "Total": 262036,
                    "Conventional": 260290,
                    "Group quarters": 1746
                },
                "Land Area (Sq Km)": 3153,
                "Density (Persons per Sq. Km)": 359
            },
            "MIGORI": {
                "Total": 1116436,
                "Sex": {
                    "Male": 536187,
                    "Female": 580214,
                    "Intersex": 35
                },
                "Households": {
                    "Total": 240168,
                    "Conventional": 238133,
                    "Group quarters": 2035
                },
                "Land Area (Sq Km)": 2613,
                "Density (Persons per Sq. Km)": 427
            },
            "KISII": {
                "Total": 1266860,
                "Sex": {
                    "Male": 605784,
                    "Female": 661038,
                    "Intersex": 38
                },
                "Households": {
                    "Total": 308054,
                    "Conventional": 307254,
                    "Group quarters": 800
                },
                "Land Area (Sq Km)": 1323,
                "Density (Persons per Sq. Km)": 957
            },
            "NYAMIRA": {
                "Total": 605576,
                "Sex": {
                    "Male": 290907,
                    "Female": 314656,
                    "Intersex": 13
                },
                "Households": {
                    "Total": 150669,
                    "Conventional": 150499,
                    "Group quarters": 170
                },
                "Land Area (Sq Km)": 897,
                "Density (Persons per Sq. Km)": 675
            },
            "NAIROBI CITY": {
                "Total": 4397073,
                "Sex": {
                    "Male": 2192452,
                    "Female": 2204376,
                    "Intersex": 245
                },
                "Households": {
                    "Total": 1506888,
                    "Conventional": 1494676,
                    "Group quarters": 12212
                },
                "Land Area (Sq Km)": 704,
                "Density (Persons per Sq. Km)": 6247
            }
        }
        
    def get_kenyan_counties(self):
        return self.kenyan_counties
    