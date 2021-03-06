from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from api.models import FileUpload
from accounts.models import DocViews

# Create your views here.

SubjectMapping = {
    "cse" : "Computer Science Engineering",
    "mechanical":"Mechanical Engineering",
    "civil":"Civil Engineering",
    "electrical":"Electrical Engineering",
    "etc":"Electronics and Telecommunication Engineering",
    "metallurgy":"Metallurgical Engineering",
    "chemical":"Chemical Engineering",
    "production":"Production Engineering",
    "mining" : "Mining engineering",
}

SubjectArchive = {
    "cse": [
        {"code" : "M-I","name":"Applied Mathematics-I","type":"common"},
        {"type":"common","code":"Phy","name":"Applied Physics"},
        {"type":"common","code":"BE","name":"Basic Electronics"},
        {"type":"common","code":"BCE","name":"Basic Civil Engg"},
        {"type":"prog core","code":"C","name":"C Programming"},
        {"type":"common","code":"English","name":"English Comm Skills"},
        {"type":"common","code":"WS","name":"Engg Workshop"},
        {"type":"common","code":"Chem","name":"Applied Chemistry"},
        {"type":"common","code":"BEE","name":"Basic Electrical Engg"},
        {"type":"common","code":"BME","name":"Basic Mechanical Engg"},
        {"type":"prog core","code":"DS","name":"Data Structure"},
        {"type":"common","code":"ED","name":"Engg Drawing"},
        {"type":"common","code":"STLD","name":"Digital Electronics"},
        {"type":"prog core","code":"Java","name":"Programming using JAVA"},
        {"type":"core","code":"SP","name":"System Programming"},
        {"type":"core","code":"SE","name":"Software Engg"},
        {"type":"core","code":"DS","name":"Discrete Mathematics"},
        {"type":"common","code":"EE","name":"Engg Economics"},
        {"type":"core","code":"COA","name":"Computer Architecture"},
        {"type":"core","code":"DAA","name":"Algorithm"},
        {"type":"core","code":"DBMS","name":"Database Managemant System"},
        {"type":"core","code":"FLAT","name":"Theory Of Computation"},
        {"type":"common","code":"OB","name":"Organisational Behaviour"},
        {"type":"core","code":"OS","name":"Operating System"},
        {"type":"core","code":"CG","name":"Computer Graphics"},
        {"type":"core","code":"ACA","name":"Advanced Computer Architecture"},
        {"type":"core","code":"CC","name":"Cloud Computing"},
        {"type":"core","code":"DMDW","name":"Data Mining Data Warehousing"},
        {"type":"core","code":"CN","name":"Computer Networks"},
        {"type":"core","code":"CD","name":"Compiler Design"},
        {"type":"core","code":"WSN","name":"Wireless Sensor Network"},
        {"type":"core","code":"ML","name":"Machine Learning"},
        {"type":"common","code":"EVS","name":"Environmental Science"},
        {"type":"core","code":"CNS","name":"Cryptography and Network Security"},
        {"type":"core","code":"SC","name":"Soft Computing"},
        {"type":"core","code":"IoT","name":"Internet of Things"},
        {"type":"common","code":"GT","name":"Green Technology"},
        {"type":"common","code":"ET","name":"Entrepreneurship Training"}
    ],
    "mechanical":[

        {"code":"ADE","name":"Analog And Digital Electronics","type":"core"},
        {"code":"AE","name":"Automobile Engineering","type":"core"},
        {"code":"BC","name":"Business Communication","type":"core"},
        {"code":"BCE","name":"Basics Of Civil Engineering","type":"core"},
        {"code":"BE","name":"Basic Electronics","type":"core"},
        {"code":"BEE","name":"Basic Electrical Engineering","type":"core"},
        {"code":"BME","name":"Basics Of Mechanical Engineering","type":"core"},
        {"code":"BMP","name":"Basic Manufacturing Process","type":"core"},
        {"code":"C","name":"Programming In C","type":"core"},
        {"code":"CAC","name":"CAD AND CAM","type":"core"},
        {"code":"CADM","name":"Computer Aided Design And Manufacturing","type":"core"},
        {"code":"CE","name":"Communicative English","type":"core"},
        {"code":"CHEM","name":"Applied Chemistry","type":"core"},
        {"code":"CIM","name":"Computer Integrated Manufacturing","type":"core"},
        {"code":"DME","name":"Design Of Machine Elements","type":"core"},
        {"code":"DSP","name":"Digital Signal Processing","type":"core"},
        {"code":"EC","name":"Engineering Chemistry","type":"core"},
        {"code":"ECS","name":"English Communication Skills","type":"core"},
        {"code":"ECT","name":"Energy Conversion Techniques","type":"core"},
        {"code":"EDC","name":"Electrical Drives And Controls","type":"core"},
        {"code":"EE","name":"Engineering Economics","type":"core"},
        {"code":"EE","name":"Environmental Engineering","type":"core"},
        {"code":"EEE","name":"Electrical And Electronics Engineering","type":"core"},
        {"code":"EG","name":"ENGINEERING GRAPHICS","type":"core"},
        {"code":"EG","name":"Engineering Graphics","type":"core"},
        {"code":"EM","name":"Engineering Mechanics","type":"core"},
        {"code":"EM-2","name":"Engineering Mathematics 2","type":"core"},
        {"code":"EM1","name":"Engineering Mathematics 1","type":"core"},
        {"code":"EMM","name":"Engineering Metrology And Measurements","type":"core"},
        {"code":"EMPD","name":"Electrical Machines And Power Devices","type":"core"},
        {"code":"EP","name":"Engineering Physics","type":"core"},
        {"code":"ESE","name":"Environment Science And Engineering","type":"core"},
        {"code":"ESHC","name":"Environmental Studies And Health Care","type":"core"},
        {"code":"ET","name":"Engineering Thermodynamics","type":"core"},
        {"code":"ET","name":"Engineering Tribology","type":"core"},
        {"code":"EW","name":"Engineering Workshop","type":"core"},
        {"code":"FCF","name":"Fatigue Creep ","type":"core"},
        {"code":"FDHM","name":"Fluid Dynamics And Hydraulic Machines","type":"core"},
        {"code":"FM","name":"Fluid Mechanics","type":"core"},
        {"code":"FMHM","name":"Fluid Mechanics And Hydraulic Machines","type":"core"},
        {"code":"FMM","name":"Fluid Mechanics And Machinery","type":"core"},
        {"code":"HMF","name":"Heat ","type":"core"},
        {"code":"HT","name":"Heat Transfer","type":"core"},
        {"code":"ICEG","name":"IC Engines And Gas Turbines","type":"core"},
        {"code":"IPM","name":"Introduction To Physical Metallurgy And Engineering Materials","type":"core"},
        {"code":"IWT","name":"Internet And Web-Technologies","type":"core"},
        {"code":"KDM","name":"Kinematics And Dynamics Of Machines","type":"core"},
        {"code":"KKM","name":"Kinematic And Kinetics Of Machines","type":"core"},
        {"code":"M-1","name":"Applied Mathematics-1","type":"core"},
        {"code":"M-2","name":"Applied Mathematics - 2","type":"core"},
        {"code":"M-3","name":"Mathematics-3","type":"core"},
        {"code":"M-4","name":"Mathematics-4","type":"core"},
        {"code":"MCTD","name":"Metal Cutting And Tool Design","type":"core"},
        {"code":"MD","name":"Machine Dynamics","type":"core"},
        {"code":"MDHP","name":"Machine Dynamics And Heat Power Lab","type":"core"},
        {"code":"MECH","name":"Mechanics","type":"core"},
        {"code":"MEMS","name":"Micro-Electro-Mechanical Systems","type":"core"},
        {"code":"MIS","name":"Management Information System","type":"core"},
        {"code":"MM","name":"Marketing Management","type":"core"},
        {"code":"MM","name":"Mechanism And Machines","type":"core"},
        {"code":"MM","name":"Metrology And Measurements","type":"core"},
        {"code":"MMMR","name":"Mechanical Measurement Metallurgy And Reliability","type":"core"},
        {"code":"MOS","name":"Mechanics Of Solid","type":"core"},
        {"code":"MQCR","name":"Metrology Quality Control And Reliability","type":"core"},
        {"code":"MS","name":"Material Science","type":"core"},
        {"code":"MST","name":"Machining Science And Technology","type":"core"},
        {"code":"MT-1","name":"Manufacturing Technology- 1","type":"core"},
        {"code":"MV","name":"Mechanical Vibration","type":"core"},
        {"code":"NCES","name":"Non-Conventional Energy Systems","type":"core"},
        {"code":"NM","name":"Numerical Methods","type":"core"},
        {"code":"OB","name":"Organizational Behaviour","type":"core"},
        {"code":"OE","name":"Optimization In Engineering","type":"core"},
        {"code":"OOP","name":"Object Oriented Programming Using Cpp","type":"core"},
        {"code":"PDPT","name":"Production Design And Production Tooling","type":"core"},
        {"code":"PE","name":"Professional Ethics","type":"core"},
        {"code":"PHY","name":"Applied Physics","type":"core"},
        {"code":"PM","name":"Project Management","type":"core"},
        {"code":"POM","name":"Principles Of Management","type":"core"},
        {"code":"POM","name":"Production And Operation Management","type":"core"},
        {"code":"PPCE","name":"PROCESS PLANNING AND COST ESTIMATION","type":"core"},
        {"code":"PPE","name":"Power Plant Engineering","type":"core"},
        {"code":"PSPP","name":"Problem Solving And Python Programming","type":"core"},
        {"code":"RAC","name":"Refrigeration And Air Conditioning","type":"core"},
        {"code":"RRA","name":"Robotics And Robot Applications","type":"core"},
        {"code":"SC","name":"Soft Computing","type":"core"},
        {"code":"TD","name":"Thermodynamics","type":"core"},
        {"code":"TE","name":"Technical English","type":"core"},
        {"code":"TE-II","name":"Thermal Engineering- II","type":"core"},
        {"code":"TPDE","name":"Transform And Partial Differential Equations","type":"core"},
        {"code":"WSN","name":"Wireless Sensor Network","type":"core"},
        {"code":"PHY","name":"Applied Physics","type":"core"},

    ],
    "civil":[
        {"code":"PHY","name":"Applied Physics","type":"core"},
        {"code":"ECS","name":"English Communication Skills","type":"core"},
        {"code":"C","name":"Programming In C","type":"core"},
        {"code":"M-1","name":"Applied Mathematics-1","type":"core"},
        {"code":"BE","name":"Basic Electronics","type":"core"},
        {"code":"BEE","name":"Basic Electrical Engineering","type":"core"},
        {"code":"CHEM","name":"Applied Chemistry","type":"core"},
        {"code":"M-2","name":"Applied Mathematics - 2","type":"core"},
        {"code":"BCE","name":"Basics Of Civil Engineering","type":"core"},
        {"code":"PE","name":"Professional Ethics","type":"core"},
        {"code":"BME","name":"Basics Of Mechanical Engineering","type":"core"},
        {"code":"ESHC","name":"Environmental Studies And Health Care","type":"core"},
        {"code":"EEE","name":"Electrical And Electronics Engineering","type":"core"},
        {"code":"BME","name":"Basics Of Mechanical Engineering","type":"core"},
        {"code":"ESHC","name":"Environmental Studies And Health Care","type":"core"},
        {"code":"EEE","name":"Electrical And Electronics Engineering","type":"core"},
        {"code":"EE","name":"Engineering Economics","type":"core"},
        {"code":"OB","name":"Organizational Behaviour","type":"core"},
        {"code":"FMHM","name":"Fluid Mechanics And Hydraulic Machines","type":"core"},
        {"code":"MOS","name":"Mechanics Of Solid","type":"core"},
        {"code":"S-1","name":"Surveying-1","type":"core"},
        {"code":"GTE-1","name":"Geotechnical Engineering- 1","type":"core"},
        {"code":"CT","name":"Construction Technology","type":"core"},
        {"code":"M-3","name":"Mathematics-3","type":"core"},
        {"code":"TE1","name":"Transportation Engineering 1","type":"core"},
        {"code":"SA-1","name":"Structural Analysis-1","type":"core"},
        {"code":"AMOS","name":"Advanced Mechanics Of Solids","type":"core"},
        {"code":"SA-1","name":"Structural Analysis-1","type":"core"},
        {"code":"AMOS","name":"Advanced Mechanics Of Solids","type":"core"},
        {"code":"DCS","name":"Design Of Concrete Structures","type":"core"},
        {"code":"MT","name":"Material Testing","type":"core"},
        {"code":"DSS","name":"Design Of Steel Structure","type":"core"},
        {"code":"WSSE","name":"Water Supply And Sanitary Engineering","type":"core"},
        {"code":"WRE","name":"Water Resources Engineering","type":"core"},
        {"code":"SA-2","name":"Structural Analysis-2","type":"core"},
        {"code":"EES","name":"Environmental Engineering And Safety","type":"core"},
        {"code":"IE","name":"Irrigation Engineering","type":"core"},
        {"code":"TE 2","name":"Transportation Engineering 2","type":"core"},
        {"code":"FE","name":"Foundation Engineering","type":"core"},
        {"code":"FEM","name":"Finite Element Methods","type":"core"},
        {"code":"PCS","name":"Prestressed Concrete Structures","type":"core"},
        {"code":"SC","name":"Soft Computing","type":"core"},
        {"code":"GIT","name":"Ground Improvement Techniques","type":"core"},
        {"code":"PHY","name":"Applied Physics","type":"core"},
        {"code":"HTE","name":"Highway And Traffic Engineering","type":"core"},
        {"code":"ATE","name":"Advanced Transportation Engineering","type":"core"},
        {"code":"MATH","name":"Pure Applied Mathematics For Specific Branch Of Engineering","type":"core"},
        {"code":"GWH","name":"Ground Water Hydrology","type":"core"},
        {"code":"OCF","name":"Open Channel Flow","type":"core"},
        {"code":"PD","name":"Pavement Design","type":"core"},
        {"code":"SD","name":"Structural Dynamics","type":"core"},
        {"code":"MTS","name":"Mass Transit System","type":"core"},
        {"code":"ITA","name":"Internet Technologies And Applications","type":"core"},
        {"code":"MM","name":"Marketing Management","type":"core"},
        {"code":"POM","name":"Production And Operation Management","type":"core"},
        {"code":"WRE","name":"Water Resources Engineering","type":"core"},
        {"code":"FEM","name":"Finite Element Methods","type":"core"},
        {"code":"CEPM","name":"Construction Equipments Planning And Management","type":"core"},
        {"code":"MIS","name":"Management Information System","type":"core"},
        {"code":"GIT","name":"Ground Improvement Techniques","type":"core"},
        {"code":"AFE","name":"Advanced Foundation Engineering","type":"core"},
        {"code":"PCS","name":"Prestressed Concrete Structures","type":"core"},
        {"code":"HTE","name":"Highway And Traffic Engineering","type":"core"},
        {"code":"SD","name":"Structural Dynamics","type":"core"},
        {"code":"BCE","name":"Basics Of Civil Engineering","type":"core"},
        {"code":"PE","name":"Professional Ethics","type":"core"},
        {"code":"BME","name":"Basics Of Mechanical Engineering","type":"core"},
        {"code":"ESHC","name":"Environmental Studies And Health Care","type":"core"},
        {"code":"EEE","name":"Electrical And Electronics Engineering","type":"core"},
        {"code":"C","name":"Programming In C","type":"core"},
        {"code":"M-1","name":"Applied Mathematics-1","type":"core"},
        {"code":"PHY","name":"Applied Physics","type":"core"},
        {"code":"BEE","name":"Basic Electrical Engineering","type":"core"},
        {"code":"MECH","name":"Mechanics","type":"core"},
        {"code":"MECH","name":"Mechanics","type":"core"},
        {"code":"BE","name":"Basic Electronics","type":"core"},
        {"code":"OOP","name":"Object Oriented Programming Using Cpp","type":"core"},
        {"code":"M-2","name":"Applied Mathematics - 2","type":"core"},
        {"code":"BC","name":"Business Communication","type":"core"},
        {"code":"CHEM","name":"Applied Chemistry","type":"core"},
        {"code":"ESE","name":"Environment Science And Engineering","type":"core"},
        {"code":"C","name":"Programming In C","type":"core"},
        {"code":"M-1","name":"Applied Mathematics-1","type":"core"},
        {"code":"PHY","name":"Applied Physics","type":"core"},
        {"code":"BC","name":"Business Communication","type":"core"},
        {"code":"CHEM","name":"Applied Chemistry","type":"core"},
        {"code":"ESE","name":"Environment Science And Engineering","type":"core"},
        {"code":"C","name":"Programming In C","type":"core"},
        {"code":"M-1","name":"Applied Mathematics-1","type":"core"},
        {"code":"PHY","name":"Applied Physics","type":"core"},
        {"code":"BEE","name":"Basic Electrical Engineering","type":"core"},
        {"code":"MECH","name":"Mechanics","type":"core"},
        {"code":"EES","name":"Environmental Engineering And Safety","type":"core"},
        {"code":"M-3","name":"Mathematics-3","type":"core"},
        {"code":"MOS","name":"Mechanics Of Solid","type":"core"},
        {"code":"BMBC","name":"Building Materials And Building Construction","type":"core"},
        {"code":"S-1","name":"Surveying-1","type":"core"},
        {"code":"FM-1","name":"Fluid Mechanics-1","type":"core"},
        {"code":"NM","name":"Numerical Methods","type":"core"},
        {"code":"TE1","name":"Transportation Engineering 1","type":"core"},
        {"code":"SA-1","name":"Structural Analysis-1","type":"core"},
        {"code":"DCS","name":"Design Of Concrete Structures","type":"core"},
        {"code":"ECPP","name":"Estimation Costing And Professional Practice","type":"core"},
        {"code":"FM2","name":"Fluid Mechanics-2","type":"core"},
        {"code":"AS","name":"Advanced Surveying","type":"core"},
        {"code":"BC","name":"Business Communication","type":"core"},
        {"code":"GTE-1","name":"Geotechnical Engineering- 1","type":"core"},
        {"code":"DSS","name":"Design Of Steel Structure","type":"core"},
        {"code":"WRE","name":"Water Resources Engineering","type":"core"},
        {"code":"CEPM","name":"Construction Equipments Planning And Management","type":"core"},
        {"code":"SA-2","name":"Structural Analysis-2","type":"core"},
        {"code":"EES","name":"Environmental Engineering And Safety","type":"core"},
        {"code":"PHY","name":"Applied Physics","type":"core"},
        {"code":"DCS","name":"Design Of Concrete Structures","type":"core"},
        {"code":"WRE","name":"Water Resources Engineering","type":"core"},
        {"code":"PHY","name":"Applied Physics","type":"core"},
        {"code":"BEE","name":"Basic Electrical Engineering","type":"core"},
        {"code":"M-3","name":"Mathematics-3","type":"core"},
        {"code":"CHEM","name":"Applied Chemistry","type":"core"},
        {"code":"ECS","name":"English Communication Skills","type":"core"},
        {"code":"EW","name":"Engineering Workshop","type":"core"},
        {"code":"C","name":"Programming In C","type":"core"},
        {"code":"M-1","name":"Applied Mathematics-1","type":"core"},
        {"code":"MECH","name":"Mechanics","type":"core"},
        {"code":"M-2","name":"Applied Mathematics - 2","type":"core"},
        {"code":"EG","name":"Engineering Graphics","type":"core"},
        {"code":"M-4","name":"Mathematics-4","type":"core"},
        {"code":"BMBC","name":"Building Materials And Building Construction","type":"core"},
        {"code":"BMBC","name":"Building Materials And Building Construction","type":"core"},
        {"code":"S-1","name":"Surveying-1","type":"core"},
        {"code":"FM","name":"Fluid Mechanics","type":"core"},
        {"code":"SOM","name":"Strength Of Materials","type":"core"},
        {"code":"EE","name":"Engineering Economics","type":"core"},
        {"code":"SA-1","name":"Structural Analysis-1","type":"core"},
        {"code":"ESE","name":"Environment Science And Engineering","type":"core"},
        {"code":"EG","name":"Engineering Geology","type":"core"},
        {"code":"CE","name":"Communicative English","type":"core"},
        {"code":"EP","name":"Engineering Physics","type":"core"},
        {"code":"EG","name":"ENGINEERING GRAPHICS","type":"core"},
        {"code":"EC","name":"Engineering Chemistry","type":"core"},
        {"code":"EM1","name":"Engineering Mathematics 1","type":"core"},
        {"code":"PSPP","name":"Problem Solving And Python Programming","type":"core"}
    ],
    "electrical":[
        {"code":"M-1","name":"Applied Mathematics-1","type":"common"},
        {"code":"PHY","name":"Applied Physics","type":"common"},
        {"code":"ECS","name":"English Communication Skills","type":"common"},
        {"code":"C","name":"Programming In C","type":"common"},
        {"code":"BE","name":"Basic Electronics","type":"common"},
        {"code":"BEE","name":"Basic Electrical Engineering","type":"common"},
        {"code":"CHEM","name":"Applied Chemistry","type":"common"},
        {"code":"M-2","name":"Applied Mathematics - 2","type":"common"},
        {"code":"BCE","name":"Basics Of Civil Engineering","type":"common"},
        {"code":"PE","name":"Professional Ethics","type":"common"},
        {"code":"BME","name":"Basics Of Mechanical Engineering","type":"common"},
        {"code":"ESHC","name":"Environmental Studies And Health Care","type":"common"},
        {"code":"EEE","name":"Electrical And Electronics Engineering","type":"common"},
        {"code":"BME","name":"Basics Of Mechanical Engineering","type":"common"},
        {"code":"ESHC","name":"Environmental Studies And Health Care","type":"common"},
        {"code":"EEE","name":"Electrical And Electronics Engineering","type":"common"},
        {"code":"AEC","name":"Analog Electronic Circuits","type":"core"},
        {"code":"EE","name":"Engineering Economics","type":"core"},
        {"code":"NT","name":"Network Theory","type":"core"},
        {"code":"M-2","name":"Applied Mathematics - 2","type":"core"},
        {"code":"CHEM","name":"Applied Chemistry","type":"core"},
        {"code":"AEC","name":"Analog Electronic Circuits","type":"core"},
        {"code":"EE","name":"Engineering Economics","type":"core"},
        {"code":"NT","name":"Network Theory","type":"core"},
        {"code":"OB","name":"Organizational Behaviour","type":"core"},
        {"code":"DEC","name":"Digital Electronics Circuit","type":"core"},
        {"code":"EM2","name":"Electrical Machines 2","type":"core"},
        {"code":"M-3","name":"Mathematics-3","type":"core"},
        {"code":"CSE","name":"Control System Engineering","type":"core"},
        {"code":"EPTD","name":"Electrical Power Transmission And Distribution","type":"core"},
        {"code":"MPMC","name":"Microprocessor And Microcontroller","type":"core"},
        {"code":"OE","name":"Optimization In Engineering","type":"core"},
        {"code":"PE","name":"Power Electronics","type":"core"},
        {"code":"OE","name":"Optimization In Engineering","type":"core"},
        {"code":"PE","name":"Power Electronics","type":"core"},
        {"code":"ODI","name":"Optoelectronics Devices And Instrumentation","type":"core"},
        {"code":"DSP","name":"Digital Signal Processing","type":"core"},
        {"code":"RES","name":"Renewable Energy System","type":"core"},
        {"code":"EES","name":"Environmental Engineering And Safety","type":"core"},
        {"code":"EM2","name":"Electrical Machines 2","type":"core"},
        {"code":"VLSI","name":"VLSI Design","type":"core"},
        {"code":"ED","name":"Electrical Drives","type":"core"},
        {"code":"ACS","name":"Advanced Control Systems","type":"core"},
        {"code":"HVDC","name":"High Voltage DC Transmission","type":"core"},
        {"code":"PSOC","name":"Power System Operation And Control","type":"core"},
        {"code":"BI","name":"Biomedical Instrumentation","type":"core"},
        {"code":"CE","name":"Communication Engineering","type":"core"},
        {"code":"EPQ","name":"Electrical Power Quality","type":"core"},
        {"code":"MC","name":"Mobile Communication","type":"core"},
        {"code":"DIP","name":"Digital Image Processing","type":"core"},
        {"code":"PSEE","name":"Power Station Engineering And Economics","type":"core"},
        {"code":"SC","name":"Soft Computing","type":"core"},
        {"code":"HVE","name":"High Voltage Engineering","type":"core"},
        {"code":"BCE","name":"Basics Of Civil Engineering","type":"core"},
        {"code":"PE","name":"Professional Ethics","type":"core"},
        {"code":"BME","name":"Basics Of Mechanical Engineering","type":"core"},
        {"code":"ESHC","name":"Environmental Studies And Health Care","type":"core"},
        {"code":"EEE","name":"Electrical And Electronics Engineering","type":"core"},
        {"code":"EMMI","name":"Electrical Measurement And Measuring Instruments","type":"core"},
        {"code":"MATH","name":"Pure Applied Mathematics For Specific Branch Of Engineering","type":"core"},
        {"code":"ADSP","name":"Advanced Digital Signal Processing","type":"core"},
        {"code":"NSBT","name":"Nano Science ","type":"core"},
        {"code":"SGPD","name":"Switch Gear ","type":"core"},
        {"code":"NSBT","name":"Nano Science ","type":"core"},
        {"code":"SGPD","name":"Switch Gear ","type":"core"},
        {"code":"AC","name":"Adaptive Control","type":"core"},
        {"code":"II","name":"Industrial Instrumentation","type":"core"},
        {"code":"EPQ","name":"Electrical Power Quality","type":"core"},
        {"code":"APE","name":"Advanced Power Electronics","type":"core"},
        {"code":"DIP","name":"Digital Image Processing","type":"core"},
        {"code":"MM","name":"Marketing Management","type":"core"},
        {"code":"PSEE","name":"Power Station Engineering And Economics","type":"core"},
        {"code":"PSP","name":"Power System Protection","type":"core"},
        {"code":"POM","name":"Production And Operation Management","type":"core"},
        {"code":"SCS","name":"Satellite Communication System","type":"core"},
        {"code":"ES","name":"Embedded System","type":"core"},
        {"code":"BCE","name":"Basics Of Civil Engineering","type":"core"},
        {"code":"PE","name":"Professional Ethics","type":"core"},
        {"code":"PE","name":"Professional Ethics","type":"core"},
        {"code":"EEE","name":"Electrical And Electronics Engineering","type":"core"},
        {"code":"CSE","name":"Control System Engineering","type":"core"},
        {"code":"MM","name":"Marketing Management","type":"core"},
        {"code":"POM","name":"Production And Operation Management","type":"core"},
        {"code":"CV","name":"Computer Vision","type":"core"},
        {"code":"ESE","name":"Environment Science And Engineering","type":"core"},
        {"code":"SG","name":"Smart Grid","type":"core"},
        {"code":"EM1","name":"Electrical Machines 1","type":"core"},
        {"code":"IPCD","name":"Industrial Process Control And Dynamics","type":"core"},
        {"code":"DEM","name":"Design Of Electrical Machines","type":"core"},
        {"code":"ECD","name":"Energy Conversion Devices","type":"core"},
        {"code":"SSD","name":"Solid State Devices","type":"core"},
        {"code":"C","name":"Programming In C","type":"core"},
        {"code":"M-1","name":"Applied Mathematics-1","type":"core"},
        {"code":"M-1","name":"Applied Mathematics-1","type":"core"},
        {"code":"PHY","name":"Applied Physics","type":"core"},
        {"code":"BEE","name":"Basic Electrical Engineering","type":"core"},
        {"code":"MECH","name":"Mechanics","type":"core"},
        {"code":"BE","name":"Basic Electronics","type":"core"},
        {"code":"OOP","name":"Object Oriented Programming Using Cpp","type":"core"},
        {"code":"M-2","name":"Applied Mathematics - 2","type":"core"},
        {"code":"BC","name":"Business Communication","type":"core"},
        {"code":"CHEM","name":"Applied Chemistry","type":"core"},
        {"code":"ESE","name":"Environment Science And Engineering","type":"core"},
        {"code":"BE","name":"Basic Electronics","type":"core"},
        {"code":"OOP","name":"Object Oriented Programming Using Cpp","type":"core"},
        {"code":"M-2","name":"Applied Mathematics - 2","type":"core"},
        {"code":"BC","name":"Business Communication","type":"core"},
        {"code":"CHEM","name":"Applied Chemistry","type":"core"},
        {"code":"ESE","name":"Environment Science And Engineering","type":"core"},
        {"code":"C","name":"Programming In C","type":"core"},
        {"code":"M-1","name":"Applied Mathematics-1","type":"core"},
        {"code":"PHY","name":"Applied Physics","type":"core"},
        {"code":"BEE","name":"Basic Electrical Engineering","type":"core"},
        {"code":"MECH","name":"Mechanics","type":"core"},
        {"code":"CE","name":"Communication Engineering","type":"core"},
        {"code":"ED","name":"Electrical Drives","type":"core"},
        {"code":"PSOC","name":"Power System Operation And Control","type":"core"},
        {"code":"AEC","name":"Analog Electronic Circuits","type":"core"},
        {"code":"M-3","name":"Mathematics-3","type":"core"},
        {"code":"EM1","name":"Electrical Machines 1","type":"core"},
        {"code":"DS","name":"Data Structure Using C","type":"core"},
        {"code":"ESE","name":"Environment Science And Engineering","type":"core"},
        {"code":"NA","name":"Network Analysis","type":"core"},
        {"code":"DEC","name":"Digital Electronics Circuit","type":"core"},
        {"code":"EM2","name":"Electrical Machines 2","type":"core"},
        {"code":"M-4","name":"Mathematics-4","type":"core"},
        {"code":"EMI","name":"Electrical Measurement And Instrumentation","type":"core"},
        {"code":"TE-1","name":"Thermal Engineering 1","type":"core"},
        {"code":"MPMC","name":"Microprocessor And Microcontroller","type":"core"},
        {"code":"PE","name":"Power Electronics","type":"core"},
        {"code":"EPTD","name":"Electrical Power Transmission And Distribution","type":"core"},
        {"code":"LCT","name":"Linear Control Theory","type":"core"},
        {"code":"IDSP","name":"Introduction To Digital Signal Processing","type":"core"},
        {"code":"EMF","name":"Electromagnetic Field","type":"core"},
        {"code":"ED","name":"Electrical Drives","type":"core"},
        {"code":"RES","name":"Renewable Energy System","type":"core"},
        {"code":"SGP","name":"Switch Gear And Protection","type":"core"},
        {"code":"IAC","name":"Industrial Automation And Control","type":"core"},
        {"code":"EE","name":"Engineering Economics","type":"core"},
        {"code":"MCA","name":"Microcontroller And Applications","type":"core"},
        {"code":"EPS","name":"Elements Of Power System","type":"core"},
        {"code":"PED","name":"Power Electronics And Drives","type":"core"},
        {"code":"CS","name":"Control System","type":"core"},
        {"code":"DSP","name":"Digital Signal Processing","type":"core"},
        {"code":"HVE","name":"High Voltage Engineering","type":"core"},
        {"code":"PSA","name":"Power System Analysis","type":"core"},
        {"code":"BE","name":"Basic Electronics","type":"core"},
        {"code":"BEE","name":"Basic Electrical Engineering","type":"core"},
        {"code":"EP","name":"Engineering Physics","type":"core"},
        {"code":"EM1","name":"Engineering Mathematics 1","type":"core"}
    ],
    "etc":[
        {"code":"M-1","name":"Applied Mathematics-1","type":"common"},
        {"code":"PHY","name":"Applied Physics","type":"common"},
        {"code":"ECS","name":"English Communication Skills","type":"common"},
        {"code":"C","name":"Programming In C","type":"common"},
        {"code":"BE","name":"Basic Electronics","type":"common"},
        {"code":"BEE","name":"Basic Electrical Engineering","type":"common"},
        {"code":"CHEM","name":"Applied Chemistry","type":"common"},
        {"code":"M-2","name":"Applied Mathematics - 2","type":"common"},
        {"code":"BCE","name":"Basics Of Civil Engineering","type":"common"},
        {"code":"PE","name":"Professional Ethics","type":"common"},
        {"code":"BME","name":"Basics Of Mechanical Engineering","type":"common"},
        {"code":"ESHC","name":"Environmental Studies And Health Care","type":"common"},
        {"code":"EEE","name":"Electrical And Electronics Engineering","type":"common"},
        {"code":"BME","name":"Basics Of Mechanical Engineering","type":"common"},
        {"code":"ESHC","name":"Environmental Studies And Health Care","type":"common"},
        {"code":"EEE","name":"Electrical And Electronics Engineering","type":"common"},
        {"code":"AEC","name":"Analog Electronic Circuits","type":"core"},
        {"code":"DEC","name":"Digital Electronics Circuit","type":"core"},
        {"code":"EE","name":"Engineering Economics","type":"core"},
        {"code":"NT","name":"Network Theory","type":"core"},
        {"code":"SS","name":"Signals And Systems","type":"core"},
        {"code":"PSD","name":"Semiconductor Devices","type":"core"},
        {"code":"OB","name":"Organizational Behaviour","type":"core"},
        {"code":"M-3","name":"Mathematics-3","type":"core"},
        {"code":"MPMC","name":"Microprocessor And Microcontroller","type":"core"},
        {"code":"EEM","name":"Electrical And Electronic Measurement","type":"core"},
        {"code":"EMT","name":"Electromagnetic Theory","type":"core"},
        {"code":"EEM","name":"Electrical And Electronic Measurement","type":"core"},
        {"code":"EMT","name":"Electromagnetic Theory","type":"core"},
        {"code":"EMPD","name":"Electrical Machines And Power Devices","type":"core"},
        {"code":"ACT","name":"Analog Communication Technique","type":"core"},
        {"code":"COA","name":"Computer Organisation And Architecture","type":"core"},
        {"code":"OE","name":"Optimization In Engineering","type":"core"},
        {"code":"ST","name":"Sensors And Transducers","type":"core"},
        {"code":"VLSI","name":"VLSI Design","type":"core"},
        {"code":"PE","name":"Power Electronics","type":"core"},
        {"code":"DSP","name":"Digital Signal Processing","type":"core"},
        {"code":"CSE","name":"Control System Engineering","type":"core"},
        {"code":"JAVA","name":"Java Programming","type":"core"},
        {"code":"FOOD","name":"Fiber Optics And Opto-electronic Devices","type":"core"},
        {"code":"EDM","name":"Electronic Devices And Modelling","type":"core"},
        {"code":"OOPJ","name":"Object Oriented Programming Using JAVA","type":"core"},
        {"code":"ES","name":"Embedded System","type":"core"},
        {"code":"DCCN","name":"Data Communication And Computer Network","type":"core"},
        {"code":"DSP","name":"Digital Signal Processing","type":"core"},
        {"code":"DCT","name":"Digital Communication Techniques","type":"core"},
        {"code":"OS","name":"Operating Systems","type":"core"},
        {"code":"MC","name":"Mobile Communication","type":"core"},
        {"code":"CNS","name":"Cryptography And Network Security","type":"core"},
        {"code":"RRA","name":"Robotics And Robot Applications","type":"core"},
        {"code":"AVLSI","name":"Analog VLSI Design","type":"core"},
        {"code":"ESE","name":"Environment Science And Engineering","type":"core"},
        {"code":"AWP","name":"Antenna And Wave Propagation","type":"core"},
        {"code":"DBMS","name":"Database Management System","type":"core"},
        {"code":"BSP","name":"Biomedical Signal Processing","type":"core"},
        {"code":"ASP","name":"Adaptive Signal Processing","type":"core"},
        {"code":"DIP","name":"Digital Image Processing","type":"core"},
        {"code":"SCS","name":"Satellite Communication System","type":"core"},
        {"code":"WSN","name":"Wireless Sensor Network","type":"core"},
        {"code":"ACS","name":"Advanced Control Systems","type":"core"},
        {"code":"MC","name":"Mobile Computing","type":"core"},
        {"code":"SC","name":"Soft Computing","type":"core"},
        {"code":"ES","name":"Embedded System","type":"core"},
        {"code":"II","name":"Industrial Instrumentation","type":"core"},
        {"code":"ME","name":"Microwave Engineering","type":"core"},
        {"code":"DIP","name":"Digital Image Processing","type":"core"},
        {"code":"ITA","name":"Internet Technologies And Applications","type":"core"},
        {"code":"SCS","name":"Satellite Communication System","type":"core"},
        {"code":"WSN","name":"Wireless Sensor Network","type":"core"},
        {"code":"CNS","name":"Cryptography And Network Security","type":"core"},
        {"code":"MEMS","name":"Micro-Electro-Mechanical Systems","type":"core"},
        {"code":"AVLSI","name":"Analog VLSI Design","type":"core"},
        {"code":"BCE","name":"Basics Of Civil Engineering","type":"core"},
        {"code":"PE","name":"Professional Ethics","type":"core"},
        {"code":"PE","name":"Professional Ethics","type":"core"},
        {"code":"BME","name":"Basics Of Mechanical Engineering","type":"core"},
        {"code":"ESHC","name":"Environmental Studies And Health Care","type":"core"},
        {"code":"EEE","name":"Electrical And Electronics Engineering","type":"core"},
        {"code":"PHY","name":"Applied Physics","type":"core"},
        {"code":"C","name":"Programming In C","type":"core"},
        {"code":"MATH","name":"Pure Applied Mathematics For Specific Branch Of Engineering","type":"core"},
        {"code":"DSD","name":"Digital System Design","type":"core"},
        {"code":"M-1","name":"Applied Mathematics-1","type":"core"},
        {"code":"BEE","name":"Basic Electrical Engineering","type":"core"},
        {"code":"MECH","name":"Mechanics","type":"core"},
        {"code":"BE","name":"Basic Electronics","type":"core"},
        {"code":"OOP","name":"Object Oriented Programming Using Cpp","type":"core"},
        {"code":"M-2","name":"Applied Mathematics - 2","type":"core"},
        {"code":"OOP","name":"Object Oriented Programming Using Cpp","type":"core"},
        {"code":"M-2","name":"Applied Mathematics - 2","type":"core"},
        {"code":"BC","name":"Business Communication","type":"core"},
        {"code":"CHEM","name":"Applied Chemistry","type":"core"},
        {"code":"ESE","name":"Environment Science And Engineering","type":"core"},
        {"code":"BE","name":"Basic Electronics","type":"core"},
        {"code":"C","name":"Programming In C","type":"core"},
        {"code":"M-1","name":"Applied Mathematics-1","type":"core"},
        {"code":"PHY","name":"Applied Physics","type":"core"},
        {"code":"BEE","name":"Basic Electrical Engineering","type":"core"},
        {"code":"MECH","name":"Mechanics","type":"core"},
        {"code":"C","name":"Programming In C","type":"core"},
        {"code":"M-1","name":"Applied Mathematics-1","type":"core"},
        {"code":"PHY","name":"Applied Physics","type":"core"},
        {"code":"BEE","name":"Basic Electrical Engineering","type":"core"},
        {"code":"MECH","name":"Mechanics","type":"core"},
        {"code":"AEC","name":"Analog Electronic Circuits","type":"core"},
        {"code":"M-3","name":"Mathematics-3","type":"core"},
        {"code":"NT","name":"Network Theory","type":"core"},
        {"code":"SS","name":"Signals And Systems","type":"core"},
        {"code":"BC","name":"Business Communication","type":"core"},
        {"code":"PSD","name":"Semiconductor Devices","type":"core"},
        {"code":"ACT","name":"Analog Communication Technique","type":"core"},
        {"code":"DEC","name":"Digital Electronics Circuit","type":"core"},
        {"code":"M-4","name":"Mathematics-4","type":"core"},
        {"code":"EMI","name":"Electrical Measurement And Instrumentation","type":"core"},
        {"code":"EMI","name":"Electrical Measurement And Instrumentation","type":"core"},
        {"code":"MPMC","name":"Microprocessor And Microcontroller","type":"core"},
        {"code":"DSP","name":"Digital Signal Processing","type":"core"},
        {"code":"DCT","name":"Digital Communication Techniques","type":"core"},
        {"code":"CSE","name":"Control System Engineering","type":"core"},
        {"code":"EMT","name":"Electromagnetic Theory","type":"core"},
        {"code":"VLSI","name":"VLSI Design","type":"core"},
        {"code":"AWP","name":"Antenna And Wave Propagation","type":"core"},
        {"code":"DCCN","name":"Data Communication And Computer Network","type":"core"},
        {"code":"COA","name":"Computer Organisation And Architecture","type":"core"},
        {"code":"OS","name":"Operating Systems","type":"core"},
        {"code":"ME","name":"Microwave Engineering","type":"core"},
        {"code":"WNMC","name":"Wireless Networks And Mobile Computing","type":"core"},
        {"code":"M-1","name":"Applied Mathematics-1","type":"core"},
        {"code":"PHY","name":"Applied Physics","type":"core"},
        {"code":"PHY","name":"Applied Physics","type":"core"},
        {"code":"BEE","name":"Basic Electrical Engineering","type":"core"},
        {"code":"MECH","name":"Mechanics","type":"core"},
        {"code":"CHEM","name":"Applied Chemistry","type":"core"},
        {"code":"ECS","name":"English Communication Skills","type":"core"},
        {"code":"EW","name":"Engineering Workshop","type":"core"},
        {"code":"C","name":"Programming In C","type":"core"},
        {"code":"M-3","name":"Mathematics-3","type":"core"},
        {"code":"M-2","name":"Applied Mathematics - 2","type":"core"},
        {"code":"EG","name":"Engineering Graphics","type":"core"},
        {"code":"AEC","name":"Analog Electronic Circuits","type":"core"},
        {"code":"DSP","name":"Digital Signal Processing","type":"core"},
        {"code":"M-4","name":"Mathematics-4","type":"core"},
        {"code":"ESE","name":"Environment Science And Engineering","type":"core"},
        {"code":"ACT","name":"Analog Communication Technique","type":"core"},
        {"code":"ACT","name":"Analog Communication Technique","type":"core"},
        {"code":"DEC","name":"Digital Electronics Circuit","type":"core"},
        {"code":"EE","name":"Engineering Economics","type":"core"},
        {"code":"CSE","name":"Control System Engineering","type":"core"},
        {"code":"STLD","name":"Switching Theory And Logic Design","type":"core"},
        {"code":"CG","name":"Computer Graphics","type":"core"},
        {"code":"CE","name":"Communicative English","type":"core"},
        {"code":"EP","name":"Engineering Physics","type":"core"},
        {"code":"EC","name":"Engineering Chemistry","type":"core"},
        {"code":"EM1","name":"Engineering Mathematics 1","type":"core"},
        {"code":"PSPP","name":"Problem Solving And Python Programming","type":"core"},
        {"code":"EG","name":"ENGINEERING GRAPHICS","type":"core"},
        {"code":"EM-2","name":"Engineering Mathematics 2","type":"core"},
        {"code":"TE","name":"Technical English","type":"core"},
        {"code":"PEE","name":"Physics Of Electronics Engineering","type":"core"},
        {"code":"BEIE","name":"Basic Electrical And Instrumentation Engineering","type":"core"},
        {"code":"CA","name":"Circuit Analysis","type":"core"},
        {"code":"ED","name":"Electronics Devices","type":"core"},
        {"code":"CSE","name":"Control System Engineering","type":"core"},
        {"code":"SS","name":"Signal And Systems","type":"core"},
        {"code":"LAPDE","name":"Linear Algebra And Partial Differential Equations","type":"core"},
        {"code":"EC-1","name":"Electronic Circuits-I","type":"core"},
        {"code":"PRP","name":"Probability And Random Processes","type":"core"},
        {"code":"ESE","name":"Environment Science And Engineering","type":"core"},
        {"code":"EMF","name":"Electromagnetic Field","type":"core"},
        {"code":"LIC","name":"Linear Integrated Circuits","type":"core"},
        {"code":"EC-2","name":"Electronic Circuits-2","type":"core"},
        {"code":"CT","name":"Communication Theory","type":"core"},
        {"code":"OOP","name":"Object Oriented Programming Using Cpp","type":"core"},
        {"code":"OS","name":"Operating Systems","type":"core"},
        {"code":"CAO","name":"Computer Architecture Organisation","type":"core"},
        {"code":"TQM","name":"Total Quality Management","type":"core"}
    ],
    "chemical":[
        {"code":"M-1","name":"Applied Mathematics-1","type":"common"},
        {"code":"PHY","name":"Applied Physics","type":"common"},
        {"code":"ECS","name":"English Communication Skills","type":"common"},
        {"code":"C","name":"Programming In C","type":"common"},
        {"code":"BE","name":"Basic Electronics","type":"common"},
        {"code":"BEE","name":"Basic Electrical Engineering","type":"common"},
        {"code":"CHEM","name":"Applied Chemistry","type":"common"},
        {"code":"M-2","name":"Applied Mathematics - 2","type":"common"},
        {"code":"BCE","name":"Basics Of Civil Engineering","type":"common"},
        {"code":"PE","name":"Professional Ethics","type":"common"},
        {"code":"BME","name":"Basics Of Mechanical Engineering","type":"common"},
        {"code":"ESHC","name":"Environmental Studies And Health Care","type":"common"},
        {"code":"EEE","name":"Electrical And Electronics Engineering","type":"common"},
        {"code":"BME","name":"Basics Of Mechanical Engineering","type":"common"},
        {"code":"ESHC","name":"Environmental Studies And Health Care","type":"common"},
        {"code":"EEE","name":"Electrical And Electronics Engineering","type":"common"},
        {"code":"FFFM","name":"Fluid Flow & Flow Measurement ","type":"core"},
        {"code":"CT","name":" Chemical Technology ","type":"core"},
        {"code":"MO","name":" Mechanical Operation ","type":"core"},
        {"code":"MT-I","name":" Mass Transfer-I ","type":"core"},
        {"code":"CP","name":" Chemical Process ","type":"core"},
        {"code":"EE","name":" Engineering Economics ","type":"core"},
        {"code":"PAM","name":" Purely Applied Mathematics ","type":"core"},
        {"code":"MT-II","name":" Mass Transfer-II ","type":"core"},
        {"code":"HT","name":" Heat Transfer ","type":"core"},
        {"code":"CET","name":" Chemical Engg. Thermodynamics ","type":"core"},
        {"code":"FET","name":" Fuel & Energyy Technology ","type":"core"},
        {"code":"EEOB","name":" Engineering Economics/Organizational Behavior ","type":"core"},
        {"code":"TP","name":" Transport Phenomena ","type":"core"},
        {"code":"PED","name":" Process Equipment Design ","type":"core"},
        {"code":"CRE","name":" Chemical Reaction Engg. ","type":"core"},
        {"code":"PIPSM","name":" Process Instrumentaion/Process Simulation & Modelling ","type":"core"},
        {"code":"BFB ","name":" Biotechnology/Food Biotechnology  ","type":"core"},
        {"code":"AL-I","name":" Advance Lab-I ","type":"core"},
        {"code":"NM-MATLAB","name":" Numerical Methods & MATLAB ","type":"core"},
        {"code":"PDC","name":" Process Dynamics & Control","type":"core"},
        {"code":"FoBEFE","name":" Fundamentals of Biochemical Engg./FluidizationEngg.","type":"core"},
        {"code":"PT","name":" Polymer Technogy","type":"core"},
        {"code":"sT","name":" separation Technology","type":"core"},
        {"code":"ESE","name":" GS Environmental Science & Engineering","type":"core"},
        {"code":"IL","name":" Industrial Lecture ","type":"core"},
        {"code":"NSBT","name":" Nano Science & Bio Technology","type":"core"},
        {"code":"PPT","name":" Pulp & Paper Technology","type":"core"},
        {"code":"PRE","name":" Petroleum Refinery Engg.","type":"core"},
        {"code":"MP","name":" Mineral Processing","type":"core"},
        {"code":"PTGTNT","name":" Pinch Technology/Green Technology/Nano-Technology","type":"core"},
        {"code":"SC","name":" Soft Computing ","type":"core"},
        {"code":"ALIIP","name":" Advance Lab-II/ Project ","type":"core"},
        {"code":"IoT","name":" Internet of Things","type":"core"}
    ],
    "metallurgy":[{"code":"404","name":"Coming Soon","type":"core"}],
    "production":[{"code":"404","name":"Coming Soon","type":"core"}]

}


cse_code_subject_mapping = {
    "M-I":"Applied Mathematics-I","Phy":"Applied Physics","BE":"Basic Electronics","BCE":"Basic Civil Engg","C":"C Programming","English":"English Comm Skills","WS":"Engg Workshop","Chem":"Applied Chemistry","BEE":"Basic Electrical Engg","BME":"Basic Mechanical Engg","DS":"Data Structure","ED":"Engg Drawing","STLD":"Digital Electronics","Java":"Programming using JAVA","SP":"System Programming","SE":"Software Engg","DS":"Discrete Mathematics","EE":"Engg Economics","COA":"Computer Architecture","DAA":"Algorithm","DBMS":"Database Managemant System","FLAT":"Formal Language and Automata Theory","OB":"Organisational Behaviour","OS":"Operating System","CG":"Computer Graphics","ACA":"Advanced Computer Architecture","CC":"Cloud Computing","DMDW":"Data Mining Data Warehousing","CN":"Computer Networks","CD":"Compiler Design","WSN":"Wireless Sensor Network","ML":"Machine Learning","EVS":"Environmental Science","CNS":"Cryptography and Network Security","SC":"Soft Computing","IoT":"Internet of Things","GT":"Green Technology","ET":"Entrepreneurship Training"
}





''' Index Page '''

def index(request):
    if request.user.is_authenticated:
        return render(request, 'home.html',{"subjects":SubjectMapping})
    else:
        return render(request, 'index.html')



''' Explore Page '''

def explore(request):
    subject_code = request.GET.get('sub')
    subjects = {}
    subject_name = ""
    if subject_code is not None:
        subjects = SubjectArchive.get(subject_code)
        subject_name = SubjectMapping.get(subject_code)

    return render(request, 'subject.html',{"subjects" : subjects,"name":subject_name})




''' Details of a Subject '''
def sub_details(request):
    subject_code = request.GET.get('sub')

    subject_name = ""
    if subject_code is not None:
        subject_name = cse_code_subject_mapping.get(subject_code)
    
    files = FileUpload.objects.filter(subject_code = subject_code.upper())

    notes = []
    pyqs = []
    gate_pyqs = []

    for file in files:
        if file.documentType == 'Notes':
            notes.append(file)
        elif file.documentType == 'PYQ':
            pyqs.append(file)
        else:
            gate_pyqs.append(file)

    return render(request,"subjectDetails.html",{"notes":notes,"pyqs":pyqs,"gate_pyqs":gate_pyqs})



def contentView(request):

    file_id = request.GET.get('id')
    
    file = FileUpload.objects.get(pk=file_id)

    if request.user.is_authenticated:
        visit = DocViews(username=request.user,visit_id=file_id)
        visit.save()

    return render(request,"subjectContent.html",{"file":file})


''' Upload Page '''

@login_required(login_url="login")
def upload(request):
    return render(request,"upload.html")



''' After login Page '''
@login_required
def afterLogin(request):


    #Most Viewed Docs Logic
    visits = {} 
    for obj in DocViews.objects.all():
        if obj.visit_id in visits:
            visits[obj.visit_id] += 1
        else:
            visits[obj.visit_id] = 1
        
    visits = dict( sorted(visits.items(), key=lambda item: item[1],reverse=True))

    most_viewed = []

    for k,v in visits.items():
        most_viewed.append(FileUpload.objects.get(pk=int(k)))

    # print(most_viewed)

    #Recommendations Logic

    file_visited = DocViews.objects.filter(username=request.user)
    user_visits = {}
    my_visit = set()

    for obj in file_visited:
        my_visit.add(obj.visit_id)
        if obj.visit_id in user_visits:
            user_visits[obj.visit_id] += 1
        else:
            user_visits[obj.visit_id] = 1
    
    user_visits = dict( sorted(user_visits.items(), key=lambda item: item[1],reverse=True))

    subject_visits = {}
    for k,v in user_visits.items():
        sub = FileUpload.objects.get(pk=int(k)).subject_code
        if sub in subject_visits:
            subject_visits[sub] += int(v)
        else:
            subject_visits[sub] = int(v)

    subject_visits = dict( sorted(subject_visits.items(), key=lambda item: item[1],reverse=True))

    recommendations = []

    for k,v in subject_visits.items():
        files = FileUpload.objects.filter(subject_code=k)
        for file in files:
            if file.id not in my_visit:
                recommendations.append(file)

    # print(recommendations)

    # Continue Reading Logic

    user_visit = set()
    recently_visited = []
    for obj in reversed(file_visited):
        if obj.visit_id not in user_visit:
            recently_visited.append(FileUpload.objects.get(pk=int(obj.visit_id)))
            user_visit.add(obj.visit_id)






    return render(request,"afterLogin.html",{"most_vieweds":most_viewed,"recommendations":recommendations,"recently_visiteds":recently_visited})


@login_required(login_url="login")
def home(request):
    return render(request, 'auth.html')

