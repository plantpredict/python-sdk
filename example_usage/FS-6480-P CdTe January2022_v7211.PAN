PVObject_=pvModule
  Version=7.211
  Flags=$00100043

  PVObject_Commercial=pvCommercial
    Comment=www.firstsolar.com   (USA)
    Flags=$0041
    Manufacturer=First Solar
    Model=FS-6480-P/FS-6480-P-I Jan2022
    DataSource=Manufacturer January. 2022
    YearBeg=2022
    Width=1.245
    Height=2.024
    Depth=0.049
    Weight=35.0
    NPieces=0
    PriceDate=02/02/2022 00:00
    Currency=EUR
    Remarks, Count=5
      Str_1=Frame: anodized aluminum frame
      Str_2=Laminate: glass-polyolefin-glass laminate
      Str_3=.
      Str_4=.
      Str_5=.
    End of Remarks=.
  End of PVObject pvCommercial

  Technol=mtCdTe
  NCelS=264
  NCelP=1
  NDiode=1
  GRef=1000
  TRef=25
  PNom=480.0
  PNomTolLow=0
  PNomTolUp=5
  Isc=2.62
  Voc=225.4
  Imp=2.49
  Vmp=192.8
  muISC=1.048
  muVocSpec=-631.1200000000001
  muPmpReq=-0.32
  RShunt=50100
  Rp_0=50100
  Rp_Exp=5.5
  RSerie=2.656
  Gamma=1.204
  D2MuTau=0.3600000000000001
  VMaxIEC=1500
  VMaxUL=1500
  Absorb=0.9
  ARev=3.2
  BRev=3.92
  RDiode=0.01
  VRevDiode=-0.7
  AirMassRef=1.5
  CellArea=88.28
  SandiaAMCorr=50.0
  RelEffic800=0.28999999999999027
  RelEffic600=0.029999999999996696
  RelEffic400=-1.2800000000000034
  RelEffic200=-5.600000000000005

  PVObject_IAM=pvIAM
    Flags=$00
    IAMMode=UserProfile
    IAMProfile=TCubicProfile
      NPtsMax=9
      NPtsEff=9
      LastCompile=$B18D
      Mode=3
      Point_1=0,1.0
      Point_2=30,1.0
      Point_3=50,0.99
      Point_4=60,0.96
      Point_5=65,0.94
      Point_6=70,0.89
      Point_7=75,0.82
      Point_8=80,0.69
      Point_9=90,0.0
    End of TCubicProfile
  End of PVObject pvIAM

  OperPoints, list of=4 tOperPoint
    Point_1=False,800,25.0,0.28999999999999027,0.00,0.000,0.000,0.00
    Point_2=False,600,25.0,0.029999999999996696,0.00,0.000,0.000,0.00
    Point_3=False,400,25.0,-1.2800000000000034,0.00,0.000,0.000,0.00
    Point_4=False,200,25.0,-5.600000000000005,0.00,0.000,0.000,0.00
  End of List OperPoints
End of PVObject pvModule
