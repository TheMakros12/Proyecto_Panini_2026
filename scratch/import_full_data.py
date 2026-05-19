import database
import re

DATA = """
00-. Logo Panini
FWC 1-. Logo Mundial - Parte Superior
FWC 2-. Logo Mundial - Parte Inferior
FWC 3-. Official Mascots
FWC 4-. Official Slogan
FWC 5-. Official Ball
FWC 6-. Canadá - Host Country Emblem
FWC 7-. México - Host Country Emblem
FWC 8-. USA - Host Country Emblem
MEX 1-. Escudo
MEX 2-. Luis Malagón 
MEX 3-. Johan Vásquez 
MEX 4-. Jorge Sánchez 
MEX 5-. César Montes 
MEX 6-. Jesús Gallardo 
MEX 7-. Israel Reyes 
MEX 8-. Diego Lainez 
MEX 9-. Carlos Rodríguez 
MEX 10-. Edson Álvarez 
MEX 11-. Orbelin Pineda 
MEX 12-. Marcel Ruiz 
MEX 13-. Foto Equipo
MEX 14-. Érick Sánchez 
MEX 15-. Hirving Lozano 
MEX 16-. Santiago Giménez
MEX 17-. Raúl Jiménez 
MEX 18-. Alexis Vega 
MEX 19-. Roberto Alvarado 
MEX 20-. César Huerta
RSA 1-. Escudo
RSA 2-. Ronwen Williams 
RSA 3-. Sipho Chaine 
RSA 4-. Aubrey Modiba
RSA 5-. Samukele Kabini
RSA 6-. Khuliso Mudau 
RSA 7-. Khulumani Ndamane
RSA 8-. Siyabonga Ngezana
RSA 9-. Khuliso Mudau 
RSA 10-. Nkosinathi Sibisi 
RSA 11-. Teboho Mokoena 
RSA 12-. Thalente Mbatha
RSA 13-. Foto Equipo
RSA 14-. Bathusi Aubaas
RSA 15-. Yaya Sithole 
RSA 16-. Sipho Mbule 
RSA 17-. Lyle Foster
RSA 18-. Iqraam Rayners
RSA 19-. Mohau Nkota 
RSA 20-. Oswin Appollis 
KOR 1. Escudo
KOR 2. Hyeonwoo Jo
KOR 3. Seunggyu Kim 
KOR 4-. Minjae Kim 
KOR 5-. Yumin Cho
KOR 6. Youngwoo Seol 
KOR 7. Hanbeom Lee 
KOR 8. Taeseok Lee 
KOR 9. Myungjae Lee 
KOR 10. Jaesung Lee 
KOR 11. Inbeom Hwang 
KOR 12. Kangin Lee 
KOR 13. Fotio Equipo
KOR 14. Seungho Paik 
KOR 15. Jens Castrop 
KOR 16-. Donggyeong Lee
KOR 17-. Guesung Cho
KOR 18-. Heungmin Son
KOR 19-. Heechan Hwang
KOR 20-. Hyeongyu Oh
CZE 1-. Escudo
CZE 2-. Matěj Kovář
CZE 3-. Jindřich Staněk
CZE 4-. Ladislav Krejčí
CZE 5-. Vladimír Coufal
CZE 6-. Jaroslav Zelený
CZE 7-. Tomáš Holeš
CZE 8-. David Zima
CZE 9-. Michal Sadílek
CZE 10-. Lukáš Provod
CZE 11-. Lukáš Červ
CZE 12-. Tomáš Souček
CZE 13-. Foto Equipo
CZE 14-. Pavel Šulc
CZE 15-. Matěj Vydra
CZE 16-. Vasil Kušej
CZE 17-. Tomáš Chorý
CZE 18-. Václav Černý
CZE 19-. Adam Hložek
CZE 20-. Patrik Schick 
CAN 1-. Escudo
CAN 2-. Dayne St. Clair 
CAN 3-. Alphonso Davies 
CAN 4-. Alistair Johnston 
CAN 5-. Samuel Adekugbe 
CAN 6-. Samuel Richie Larvea
CAN 7-. Derek Cornelius 
CAN 8-. Moïse Bombito
CAN 9-. Kamal Miller 
CAN 10-. Stephen Eustáquio 
CAN 11-. Ismaël Koné 
CAN 12-. Jonathan Osorio
CAN 13-. Foto Equipo
CAN 14-. Jacob Shaffelburg 
CAN 15-. Mathieu Choinière 
CAN 16-. Niko Sigur 
CAN 17-. Tajon Buchanan
CAN 18-. Liam Millar 
CAN 19-. Dyle Larin
CAN 20-. Jonathan David 
BIH 1-. Escudo
BIH 2-. Nikola Vasilj
BIH 3-. Amar Dedić
BIH 4-. Sead Kolašinac
BIH 5-. Tarik Muharemović
BIH 6-. Nihad Mujakić
BIH 7-. Nikola Katić
BIH 8-. Amir Hadžiahmetović
BIH 9-. Benjamin Tahirović
BIH 10-. Armin Gigović
BIH 11-. Ivan Šunjić
BIH 12-. Ivan Bašić
BIH 13-. Foto Equipo
BIH 14-. Dženis Burnić
BIH 15-. Esmir Bajraktarevic
BIH 16-. Amar Memić
BIH 17-. Ermedin Demirović
BIH 18-. Edin Džeko
BIH 19-. Samed Baždar
BIH 20-. Haris Tabaković
QAT 1-. Escudo
QAT 2-. Meshaal Barsham
QAT 3-. Sultan Albrake
QAT 4-. Lucas Mendes 
QAT 5-. Homam Ahmed
QAT 6-. Boualem Khoukhi
QAT 7-. Pedro Miguel 
QAT 8-. Tarek Salman 
QAT 9-. Mohammed Mannai
QAT 10-. Karim Boudiaf
QAT 11-. Assim Madibo
QAT 12-. Hamed Fatehi
QAT 13-. Foto Equipo
QAT 14-. Mohammed Waad
QAT 15-. Abdulaziz Hatem 
QAT 16-. Hassan Al-Haydos 
QAT 17-. Edmilson Junior
QAT 18-. Akram Hassan Afif
QAT 19-. Ahmed Al-Ganehi
QAT 20-. Almoez Ali 
SUI 1-. Escudo
SUI 2-. Gregor Kobel
SUI 3-. Yvon Mvogo
SUI 4-. Manuel Akanji 
SUI 5-. Ricardo Rodríguez
SUI 6-. Nico Elvedi 
SUI 7-. Aurèle Amenda 
SUI 8-. Silvan Widmer
SUI 9-. Granit Xhaka
SUI 10-. Denis Zakaria 
SUI 11-. Remo Freuler 
SUI 12-. Fabian Rieder
SUI 13-. Foto Equipo
SUI 14-. Ardon Jashari 
SUI 15-. Johan Manzambi
SUI 16-. Michel Aebischer
SUI 17-. Breel Embolo
SUI 18-. Rubén Vatgas
SUI 19-. Dan Ndoye 
SUI 20-. Zeki Amdouni 
BRA 1-. Escudo
BRA 2-. Alisson 
BRA 3-. Bento 
BRA 4-. Marquinhos
BRA 5-. Éder Militão 
BRA 6-. Gabriel Magalhães
BRA 7-. Danilo
BRA 8-. Wesley 
BRA 9-. Lucas Paquetá 
BRA 10-. Casemiro 
BRA 11-. Bruno Guimarães
BRA 12-. Luiz Henrique 
BRA 13-. Foto Equipo
BRA 14-. Vinicius Júnior 
BRA 15-. Rodrygo 
BRA 16-. João Pedro 
BRA 17-. Matheus Cunha 
BRA 18-. Gabriel Martinelli
BRA 19-. Raphinha 
BRA 20-. Estévão 
MAR 1-. Escudo
MAR 2-. Yassine Bounou 
MAR 3-. Munir El Kajoui
MAR 4-. Achraf Hakimi
MAR 5-. Noussair Mazraoui
MAR 6-. Nayef Aguerd
MAR 7-. Romain Saïss
MAR 8-. Jawad El Yamiq
MAR 9-. Adam Masina 
MAR 10-. Sofyan Amrabat
MAR 11-. Azzedine Ounahi
MAR 12-. Eliesse Ben Seghir
MAR 13-. Foto Equipo
MAR 14-. Bilal El Khannouss
MAR 15-. Ismael Saibari 
MAR 16-. Youssef En-Nesyri 
MAR 17-. Abde Ezzalzouli
MAR 18-. Soufiane Rahimi
MAR 19-. Brahim Díaz 
MAR 20-. Ayoub El Kaabi 
HAI 1-. Escudo
HAI 2-. Johny Placide
HAI 3-. Carlens Arcus 
HAI 4-. Martin Expérience 
HAI 5-. Jean-Kévin Duverne
HAI 6-. Ricardo Adé 
HAI 7-. Duke Lacroix 
HAI 8-. Garven Metusala
HAI 9-. Hannes Delcroix
HAI 10-. Leverton Pierre
HAI 11-. Danley Jean Jacques
HAI 12-. Jean-Ricner Bellegarde
HAI 13-. Foto Equipo
HAI 14-. Christopher Attys
HAI 15-. Derrick Etienne Jr.
HAI 16-. Josué Casimir 
HAI 17-. Ruben Providence 
HAI 18-. Duckens Nazon
HAI 19-. Louicius Deedson 
HAI 20-. Frantzdy Pierrot 
SCO 1-. Escudo
SCO 2-. Angus Gunn 
SCO 3-. Jack Hendry
SCO 4-. Kieran Tierney 
SCO 5-. Aaron Hickey 
SCO 6-. Andrew Robertson 
SCO 7-. Scott McKenna 
SCO 8-. John Souttar
SCO 9-. Anthony Ralston 
SCO 10-. Grant Hanley
SCO 11-. Scott McTominay
SCO 12-. Billy Gilmour
SCO 13-. Foto equipo 
SCO 14-. Lewis Ferguson 
SCO 15-. Ryan Christie
SCO 16-. Kenny McLean 
SCO 17-. John McGinn
SCO 18-. Lyndon Dykes
SCO 19-. Ché Adams 
SCO 20-. Ben Gannon-Doak 
USA 1-. Escudo
USA 2-. Matt Freese
USA 3-. Chris Richards
USA 4-. Tim Ream
USA 5-. Mark McKenzie 
USA 6-. Alex Freeman
USA 7-. Antonee Robinson 
USA 8-. Tyler Adams
USA 9-. Tanner Tessmann
USA 10-. Weston McKenny
USA 11-. Christian Roldan
USA 12-. Timothy Weah
USA 13-. Foto Equipo
USA 14-. Diego Luna
USA 15-. Malik Tillman
USA 16-. Christian Pulisic 
USA 17-. Brenden Aaronson
USA 18-. Ricardo Pepi
USA 19-. Haji Wright
USA 20-. Folarin Balogun
PAR 1-. Escudo
PAR 2-. Roberto Fernández
PAR 3-. Orlando Gill 
PAR 4-. Diego Gómez
PAR 5-. Fabián Balbuena
PAR 6-. Juan José Cáceres
PAR 7-. Omar Alderete 
PAR 8-. Júnior Alonso
PAR 9-. Mathías Villasanti 
PAR 10-. Diego Gómez 
PAR 11-. Damián Bobadilla
PAR 12-. Andrés Cubas
PAR 13-. Foto Equipo
PAR 14-. Matías Galarza Fonda
PAR 15-. Julio Enciso 
PAR 16-. Alejandro Romero Gamarra 
PAR 17-. Miguel Almirón
PAR 18-. Ramón Sosa
PAR 19-. Ángel Romero
PAR 20-. Antonio Sanabria 
AUS 1-. Escudo
AUS 2-. Mathew Ryan
AUS 3-. Joe Gauci
AUS 4-. Harry Souttar
AUS 5-. Alessandro Circati
AUS 6-. Jordan Bos 
AUS 7-. Aziz Behich 
AUS 8-. Cameron Burgess 
AUS 9-. Lewis Miller 
AUS 10-. Milos Degenek
AUS 11-. Jackson Irvine 
AUS 12-. Riley McGree 
AUS 13-. Team Photo 
AUS 14-. Aiden O'Neill 
AUS 15-. Connor Metcalfe
AUS 16-. Patrick Yazbek
AUS 17-. Craig Goodwin 
AUS 18-. Kusini Yengi
AUS 19-. Nestory Irankunda
AUS 20-. Mohamed Touré 
TUR 1-. Escudo
TUR 2-. Uğurcan Çakır
TUR 3-. Mert Müldür
TUR 4-. Zeki Çelik
TUR 5-. Abdülkereím Bardakgi
TUR 6-. Çağlar Söyüncü
TUR 7-. Merih Demiral
TUR 8-. Ferdi Kadıoğlu
TUR 9-. Kaan Ayhan
TUR 10-. Ismail Yüksek
TUR 11-. Hakan Çalhanoğlu
TUR 12-. Orkun Kökçü
TUR 13-. Foto Equipo
TUR 14-. Arda Güler
TUR 15-. Irfan Can Kahveci
TUR 16-. Yunus Akgün
TUR 17-. Can Uzun
TUR 18-. Barış Alper Yılmaz
TUR 19-. Kerem Aktürkoğlu
TUR 20-. Kenan Yildiz
GER 1-. Escudo
GER 2-. Marc-André ter Stegen 
GER 3-. Jonathan Tah 
GER 4-. David Raum 
GER 5-. Nico Schlotterbeck
GER 6-. Antonio Rüdiger 
GER 7-. Waldemar Anton 
GER 8-. Ridle Baku 
GER 9-. Maximilian Mittelstadt 
GER 10-. Joshua Kimmich 
GER 11-. Florian Wirtz 
GER 12-. Felix Nmecha 
GER 13-. Foto Equipo
GER 14-. Leon Goretzka 
GER 15-. Jamal Musiala
GER 16-. Serge Gnabry 
GER 17-. Kai Havertz 
GER 18-. Leroy Sané 
GER 19-. Karim Adeyemi 
GER 20.- Nick Woltemade 
CUW 1-. Escudo
CUW 2-. Eloy Room
CUW 3-. Armando Obispo
CUW 4-. Sherel Floranus 
CUW 5-. Jurien Gaari 
CUW 6-. Joshua Bremet
CUW 7-. Roshon Van Eijma
CUW 8-. Shurandy Sambo
CUW 9-. Livano Comenencia
CUW 10-. Godfried Roemeratoe
CUW 11-. Juninho Bacuna 
CUW 12-. Leandro Bacuna
CUW 13-. Foto Equipo
CUW 14-. Tahith Chong 
CUW 15-. Kenji Gorré
CUW 16-. Jearl Margaritha 
CUW 17-. Jürgen Locadia
CUW 18-. Jeremy Antonisse
CUW 19-. Gervane Kastaneer
CUW 20-. Sontje Hansen 
CIV 1-. Escudo
CIV 2-. Yahia Fofana
CIV 3-. Ghislain Konan
CIV 4-. Wilfried Singo 
CIV 5-. Odilon Kossounou 
CIV 6-. Evan Ndicka 
CIV 7-. Willy Boly 
CIV 8-. Emmanuel Agbadou 
CIV 9-. Ousmane Diomande 
CIV 10-. Franck Kessié 
CIV 11-. Seko Fofana 
CIV 12-. Ibrahim Sangaré 
CIV 13-. Foto Equipo
CIV 14-. Jean-Philippe Gbamin 
CIV 15-. Amad Diallo 
CIV 16-. Sébastien Haller
CIV 17-. Simon Adingra
CIV 18-. Yan Diomande
CIV 19-. Evann Guessand 
CIV 20-. Oumar Diakité
ECU 1-. Escudo
ECU 2-. Hernán Galíndez 
ECU 3-. Gonzalo Valle 
ECU 4-. Piero Hincapié 
ECU 5-. Pervis Estupiñán 
ECU 6-. Willian Pacho 
ECU 7-. Ángelo Preciado
ECU 8-. Joel Ordóñez 
ECU 9-. Moisés Caicedo
ECU 10-. Alan Franco
ECU 11-. Kendry Páez
ECU 12-. Pedro Vite
ECU 13-. Foto Equipo
ECU 14-. John Yeboah
ECU 15-. Leonardo Campana
ECU 16-. Gonzalo Plata 
ECU 17-. Nilson Angulo
ECU 18-. Alan Minda 
ECU 19-. Kevin Rodríguez
ECU 20-. Enner Valencia
NED 1-. Escudo
NED 2-. Bart Verbruggen
NED 3-. Virgil van Dijk
NED 4-. Micky van de Ven
NED 5-. Jurien Timber 
NED 6-. Denzel Dumfries 
NED 7-. Nathan Aké 
NED 8-. Jeremie Frimpong
NED 9-. Jan Paul van Hecke 
NED 10-. Tijjani Reijnders 
NED 11-. Ryan Gravenberch 
NED 12-. Teun Koopmeiners 
NED 13-. Foto Equipo
NED 14-. Frenkie de Jong 
NED 15-. Xavi Simons 
NED 16-. Justin Kluivert
NED 17-. Memphis Depay 
NED 18-. Donyel Malen
NED 19-. Wout Weghorst
NED 20-. Cody Gakpo
JPN 1-. Escudo
JPN 2-. Zion Suzuki
JPN 3-. Henry Heroki Mochizuki 
JPN 4-. Ayumu Seko 
JPN 5-. Junnosuke Suzuki
JPN 6-. Shogo Taniguchi 
JPN 7-. Tsuyoshi Watanabe 
JPN 8-. Kaishu Sano
JPN 9-. Yuki Soma 
JPN 10-. Ao Tanaka 
JPN 11-. Daichi Kamada
JPN 12-. Takefusa Kubo 
JPN 13-. Foto Equipo
JPN 14-. Ritsu Doan 
JPN 15-. Keito Nakamura 
JPN 16-. Takumi Minamino 
JPN 17-. Shuto Machino 
JPN 18-. Junya Ito
JPN 19-. Koki Ogawa 
JPN 20-. Ayase Ueda 
SWE 1-. Escudo
SWE 2-. Viktor Johansson
SWE 3-. Isak Hien
SWE 4-. Gabriel Dudmundsson
SWE 5-. Emil Holm
SWE 6-. Voctor Nilsson Lindelöf
SWE 7-. Gustaf Lagerbielke
SWE 8-. Lucas Bergvall
SWE 9-. Hugo Larsson
SWE 10-. Jesper Karlström
SWE 11-. Yasin Ayari
SWE 12-. Mattias Svanberg
SWE 13-. Foto Equipo
SWE 14-. Daniel Svensson
SWE 15-. Ken Sema
SWE 16-. Roony Bardghji
SWE 17-. Dejan Kulusevski
SWE 18-. Anthony Elanga
SWE 19-. Alexander Isak
SWE 20-. Viktor Gvökeres
TUN 1-. Escudo
TUN 2-. Bechir Ben Saïd 
TUN 3-. Aymen Dahmen
TUN 4-. Van Valery
TUN 5-. Montassar Talbi
TUN 6-. Yassine Meriah
TUN 7-. Ali Abdi
TUN 8-. Dylan Bronn
TUN 9-. Ellyes Skhiri
TUN 10-. Aïssa Laïdouni
TUN 11-. Ferjani Sassi 
TUN 12-. Mohamed Ali Ben Romdhane
TUN 13-. Foto Equipo
TUN 14-. Hannibal Mejbri 
TUN 15-. Elias Achouri 
TUN 16-. Elias Saad 
TUN 17-. Hazem Mastouri
TUN 18-. Ismaël Gharbi
TUN 19-. Sayfallah Ltaief
TUN 20-. Naïm Sliti
BEL 1-. Escudo
BEL 2-. Thibaut Courtois
BEL 3-. Arthur Theate 
BEL 4-. Timothy Castagne 
BEL 5-. Zeno Debast 
BEL 6-. Bradon Mechele
BEL 7-. Maxim De Cuyper
BEL 8-. Thomas Meunier 
BEL 9-. Youri Tieleman 
BEL 10-. Amadou Onana 
BEL 11-. Nicolas Raskin 
BEL 12-. Alexis Saelemaekers
BEL 13-. Foto Equipo
BEL 14-. Hans Vanaken 
BEL 15-. Kevin De Bruyne 
BEL 16-. Jërërmy Doku
BEL 17-. Charles de Ketelaere 
BEL 18-. Leandro Trossard 
BEL 19-. Loïs Openda 
BEL 20-. Romelu Lukaku
EGY 1-. Escudo
EGY 2-. Mohamed Elshenawy
EGY 3-. Mohamed Hany 
EGY 4-. Mohamed Hamdy
EGY 5-. Yasser Ibrahim 
EGY 6-. Khaled Sobhi
EGY 7-. Ramy Rabia
EGY 8-. Hossam Abdelmaguid
EGY 9-. Ahmes Fatouh
EGY 10-. Marwan Attia
EGY 11-. Zizo 
EGY 12-. Hamdy Fathy 
EGY 13-. Foto Equipo
EGY 14-. Mohanad Lasheen
EGY 15-. Emam Ashour 
EGY 16-. Osama Faisal 
EGY 17-. Mohamed Salah 
EGY 18-. Mostafa Mohamed
EGY 19-. Trezeguet
EGY 20-. Omar Marsmoush 
IRN 1-. Escudo
IRN 2-. Alireza Beiranvand
IRN 3-. Morteza Pouraliganji 
IRN 4-. Ehsan Hajsafi 
IRN 5-. Milad Mohammadi
IRN 6-. Shojae Khalilzadeh
IRN 7-. Ramin Rezaeian 
IRN 8-. Hossein Kanaani 
IRN 9-. SAdegh Moharrami
IRN 10-. Saleh Hardani
IRN 11-. Saeed Ezatolahi 
IRN 12-. Saman Ghoddos
IRN 13-. Foto Equipo
IRN 14-. Omid Noorafkan
IRN 15-. Roozbeh Cheshmi 
IRN 16-. Mohammad Mohebi
IRN 17-. Sardar Azmoun
IRN 18-. Mehdi Taremi 
IRN 19-. Alireza Jahanbakhsh
IRN 20-. Ali Gholizadeh 
NZL 1-. Escudo
NZL 2-. Max Crocombe
NZL 3-. Alex Paulsen 
NZL 4-. Michael Boxall 
NZL 5-. Liberato Cacace
NZL 6-. Tim Payne 
NZL 7-. Tyler Bindon
NZL 8-. Francis de Vries
NZL 9-. Finn Surman 
NZL 10-. Joe Bell 
NZL 11-. Sarpreet Singh
NZL 12-. Ryan Thomas
NZL 13-. Team Photo 
NZL 14-. Matthew Garbett 
NZL 15-. Marko Stamenić 
NZL 16-. Ben Old
NZL 17-. Chris Wood 
NZL 18-. Elijah Just
NZL 19-. Callum McCowatt 
NZL 20-. Kosta Barbarouses 
ESP 1-. Escudo
ESP 2-. Unai Simón 
ESP 3-. Robin Le Normand 
ESP 4-. Aymeric Laporte
ESP 5-. Dean Huijsen 
ESP 6-. Pedro Porro
ESP 7-. Dani Carvajal 
ESP 8-. Marc Cucurella 
ESP 9-. Martín Zubimendi 
ESP 10-. Rodri 
ESP 11-. Pedri 
ESP 12-. Fabián Ruiz 
ESP 13-. Foto Equipo
ESP 14-. Mikel Merino 
ESP 15-. Lamine Yamal 
ESP 16-. Dani Olmo 
ESP 17-. Nico Williams 
ESP 18-. Ferran Torres 
ESP 19-. Álvaro Morata 
ESP 20-. Mikel Oyarzabal   
CPV 1-. Escudo
CPV 2-. Vozinha 
CPV 3-. Logan Costa 
CPV 4-. Pico
CPV 5-. Dinev
CPV 6-. Steven Moreira
CPV 7-. Wagner Pina 
CPV 8-. João Paulo 
CPV 9-. Yannick Semedo  
CPV 10-. Kevin Pina
CPV 11-. Patrick Andrade 
CPV 12-. Jamiro Monteiro
CPV 13-. Foto Equipo
CPV 14-. Deroy Duarte
CPV 15-. Garry Rodrigues
CPV 16-. Jovane Cabral
CPV 17-. Ryan Mendes
CPV 18-. Dailon Livramento
CPV 19-. Willy Semedo
CPV 20-. Beb
KSA 1-. Escudo
KSA 2-. Nawaf Alaqidi 
KSA 3-. Andulrahman Alsanbi
KSA 4-. Saud Abdulhamid 
KSA 5-. Nawaf Bouwashl 
KSA 6-. Jehad Thikri 
KSA 7-. Moteb AlHarbi 
KSA 8-. Hassan Altambakti 
KSA 9-. Musab Aljuwayr 
KSA 10-. Ziyad Aljohani 
KSA 11-. Abdullah Alkhaibari 
KSA 12-. Nasser Aldawsari 
KSA 13-. Foto Equipo
KSA 14-. Saleh Abu Alshamat 
KSA 15-. Marwan Alsahafi 
KSA 16-. Salem Aldawsari 
KSA 17-  Abdulrahman Alobud
KSA 18-. Feras Albrikan
KSA 19-. Saleh Alshehri 
KSA 20-. Abdullah Alhamdan
URU 1-. Escudo
URU 2-. Sergio Rochet 
URU 3-. Santiago Mele 
URU 4-. Ronald Araújo
URU 5-. José María Giménez 
URU 6-. Sebastián Cáceres
URU 7-. Mathias Olivera
URU 8-. Guillermo Varela 
URU 9-. Nhitam Nández
URU 10-. Federico Valverde
URU 11-. Giorgian de Arrascaeta
URU 12-. Rodrigo Bentancur
URU 13-. Foto Equipo 
URU 14-. Manuel Ugarte 
URU 15-. Nicolás de la Cruz
URU 16-. Maxi Araújo
URU 17-. Darwin Núñez 
URU 18-. Federico Viñas
URU 19-. Rodrigo Aguirre
URU 20-. Facundo Pellistri 
FRA 1-. Escudo
FRA 2-. Mike Maignan
FRA 3-. Theo Hernández
FRA 4-. William Saliba 
FRA 5-. Jules Koundé
FRA 6-. Ibrahima Konaté
FRA 7-. Dayot Upamecano 
FRA 8-. Lucas Digne 
FRA 9-. Aurélien Tchouaméni
FRA 10-. Eduardo Camavinga 
FRA 11-. Manu Koné
FRA 12-. Adrien Rabiot 
FRA 13-. Foto Equipo
FRA 14-. Michael Olise 
FRA 15-. Ousmane Dembélé
FRA 16-. Bradley Barcola
FRA 17-. Désiré Doué
FRA 18-. Kingsley Coman 
FRA 19-. Hugo Ekitiké
FRA 20-. Kylian Mbappé
SEN 1-. Escudo 
SEN 2-. Eduardo Mendy 
SEN 3-. Yehvann Diouf
SEN 4-. Moussa Niakhaté 
SEN 5-. Abdoulaye Sec
SEN 6-. Ismail Jakobs 
SEN 7-. El Hadji Malick Diouf
SEN 8-. Kalidou Koulibaly 
SEN 9-. Idrissa Gana Gueye
SEN 10-. Pape Marar Sarr
SEN 11-. Pape Gueye 
SEN 12-. Habib Diarra 
SEN 13-. Foto Equipo
SEN 14-. Lamine Camara 
SEN 15-. Sadio Mané
SEN 16-. Ismaïla Sarr 
SEN 17-. Boulaye Dia
SEN 18-. Iliman Ndiaye 
SEN 19-. Nicolas Jackson
SEN 20-. Krépin Diatta
IRQ 1-. Escudo
IRQ 2-. Jalal Hassan
IRQ 3-. Rebin Sulaka
IRQ 4-. Hussein Ali
IRQ 5-. Akam Hashem
IRQ 6-. Merchas Doski
IRQ 7-. Zaid Tahseen
IRQ 8-. Manaf Younis
IRQ 9-. Zidane Iqbal
IRQ 10-. Amir Al-Ammari
IRQ 11-. Ibrahim Bavesh
IRQ 12-. Ali Jasim
IRQ 13-. Foto Equipo
IRQ 14-. Youssef Amyn
IRQ 15-. Aimar Sher
IRQ 16-. Marko Farji
IRQ 17-. Osama Rashid
IRQ 18-. Ali Al-Hamadi
IRQ 19-. Aymen Hussein
IRQ 20-. Mohanad Ali
NOR 1-. Escudo
NOR 2-. Ørjan Nyland
NOR 3-. Julian Ryerson 
NOR 4-. Leo Østigård
NOR 5-. Kristoffer Vassbakk Ajer 
NOR 6-. Marcus Holmgren Pedersen 
NOR 7-. David Møller Wolfe 
NOR 8-. Torbjørn Heggem
NOR 9-. Morten Thorsby 
NOR 10-. Martin Ødegaard 
NOR 11-. Sander Berge
NOR 12-. Andreas Schjelderup 
NOR 13-. Foto Equipo
NOR 14-. Patrick Berg 
NOR 15-. Erling Haaland
NOR 16-. Alexander Sørloth
NOR 17-  Aron Dønnum 
NOR 18-. Jørgen Strand Larsen
NOR 19-. Antonio Musa
NOR 20-. Oscar Bobb 
ARG 1-. Escudo
ARG 2-. Emiliano Martínez 
ARG 3-. Nahuel Molina 
ARG 4-. Cristian Romero 
ARG 5-. Nicolás Otamendi 
ARG 6-. Nicolás Tagliafico
ARG 7-. Leonardo Balerdi 
ARG 8-. Enzo Fernández 
ARG 9-. Alexis Mac Allister 
ARG 10-. Rodrigo de Paul 
ARG 11-. Exequiel Palacios 
ARG 12-. Leandro Paredes 
ARG 13-. Foto Equipo 
ARG 14-. Nico Paz 
ARG 15-. Franco Mastantuono 
ARG 16-. Nico González 
ARG 17-. Lionel Messi
ARG 18-. Lautaro Martínez 
ARG 19-. Julián Álvarez 
ARG 20-. Giuliano Simeone 
ALG 1-. Escudo
ALG 2-. Alexis Guendouz
ALG 3-. Ramy Bensebaini
ALG 4-. Youcef Atal
ALG 5-. Rayan Aït-Nouri
ALG 6-. Mohamed Amine Tougai 
ALG 7-. Aïssa Mandi 
ALG 8-. Ismaél Bennacer
ALG 9-. Houssem Aouar
ALG 10-. Hicham Boudaoui
ALG 11-. Ramiz Zerrouki
ALG 12-. Nabil Bentaleb
ALG 13-. Foto Equipo
ALG 14-. Farès Chaïbi
ALG 15-. Riyad Mahrez
ALG 16-. Saïd Benrahma
ALG 17-. Anis Hadj Moussa
ALG 18-. Amine Gouiri
ALG 19-. Baghdad Bounedjah
ALG 20-. Mohammed Amoura
AUT 1-. Escudo
AUT 2-. Alexander Schlager 
AUT 3-. Patrick Pentz
AUT 4-. David Alaba
AUT 5-. Kevin Danso
AUT 6-. Philipp Lienhart 
AUT 7-. Stefan Bosch 
AUT 8-. Phillipp Mwene
AUT 9-. Alexander Prass
AUT 10-. Xaver Schlager
AUT 11-. Marcel Sabitzer 
AUT 12-. Konrad Laimer
AUT 13-. Foto Equipo
AUT 14-. Florian Grillitsch 
AUT 15-. Nicolas Seiwald
AUT 16-. Romano Schmid 
AUT 17-. Patrick Wimmer
AUT 18-. Christoph Baumgartner 
AUT 19-. Michael Gregoritsch
AUT 20-. Marko Arnautović 
JOR 1-. Escudo
JOR 2-. Yazeed Abulaila
JOR 3-. Ihsan Haddad
JOR 4-. Mohammad Abu Hashish
JOR 5-. Yazan Al-Arab 
JOR 6-. Abdullah Nasib
JOR 7-. Saleem Obaid  
JOR 8-. Mohammad Abualnadi 
JOR 9-. Ibrahim Saadeh 
JOR 10-. Nizar Al-Rashdan 
JOR 11-. Noor Al-Rawabder
JOR 12-. Mohannad Abu Taha
JOR 13-. Foto Equipo
JOR 14-. Amer Jamous 
JOR 15-. Mousa Al-Taamari
JOR 16-. Yazan Al-Naimat
JOR 17-. Mahmoud Al-Mardi
JOR 18-. Ali Olwan 
JOR 19-. Mohammad Abu Zrayq 
JOR 20-. Ibrahim Sabra  
POR 1-. Escudo
POR 2-. Diogo Costa
POR 3-. José Sá
POR 4-. Rubén Dias
POR 5-. João Cancelo
POR 6-. Diogo Dalot 
POR 7-. Nuno Mendes 
POR 8-. Gonçalo Inácio
POR 9-. Bernado Silva 
POR 10-. Bruno Fernandes
POR 11-. Rubén Neves
POR 12-. Vitinha
POR 13-. Foto Equipo
POR 14-. João Neves
POR 15-. Cristiano Ronaldo 
POR 16-. Francisco Trincão
POR 17-. João Felix 
POR 18-. Gonçalo Ramos
POR 19-. Pedro Neto  
POR 20-. Rafael Leão 
COD 1-. Escudo
COD 2-. Lionel Mpasi
COD 3-. Aaron Wan-Bissaka
COD 4-. Axel Tuanzebe
COD 5-. Arthur Masuaku
COD 6-. Chancel Mbemba
COD 7-. Joris Kavembe
COD 8-. Charles Pickel
COD 9-. Ngal'ayel Mukau
COD 10-. Edo Kavembe
COD 11-. Samuel Moutoussamy
COD 12-. Noah Sadiki
COD 13-. Foto Equipo
COD 14-. Théo Bongonda
COD 15-. Meschack Elia
COD 16-. Yoane Wissa
COD 17-. Brian Cipenga
COD 18-. Fiston Mavele
COD 19-. Cédric Bakambu
COD 20-. Nathanaél Mbuku
UZB 1-. Escudo
UZB 2-. Utkir Yusupov
UZB 3-. Farrukh Sayfiev
UZB 4-. Sherzod Nasrullaev
UZB 5-. Umar Eshmurodov
UZB 6-. Husniddin Aliqulov
UZB 7-. Rustam Ashurmatov 
UZB 8-. Khojiakbar Alijonov
UZB 9-. Abdukodir Khusanov
UZB 10-. Odiljon Hamrobekov
UZB 11-. Otabek Shukurov
UZB 12-. Jamshid Iskanderov
UZB 13-. Foto Equipo
UZB 14-. Azizbek Turgunboev
UZB 15-. Khojimat Erkinov
UZB 16-. Eldor Shomurodov
UZB 17-. Oston Urunov
UZB 18-. Jalolidoin Masharipov
UZB 20-. Igor Sergeev
COL 1-. Escudo
COL 2-. Camilo Vargas
COL 3-. David Ospina
COL 4-. Dávinson Sánchez 
COL 5-. Yerry Mina 
COL 6-. Daniel Muñoz
COL 7-. Johan Mojica
COL 8-. Jhon Lucumí 
COL 9-. Santiago Arias
COL 10-. Jefferson Lerma 
COL 11-. Kevin Castaño 
COL 12-. Richard Ríos 
COL 13-. Foto Equipo
COL 14-. James Rodríguez 
COL 15-. Juan Fernando Quintero 
COL 16-. Jorge Carrascal
COL 17-. Jhon Arias
COL 18-. Jhon Córdova 
COL 19-. Luis Suárez
COL 20-. Luis Díaz 
ENG 1-. Escudo
ENG 2-. Jordan Pickford
ENG 3-. John Stones
ENG 4-. Marc Guéhi 
ENG 5-. Ezri Konsa 
ENG 6-. Trent Alexander-Arnold
ENG 7-. Reece James 
ENG 8-. Dan Burn 
ENG 9-. Jordan Henderson
ENG 10-. Declan Rice 
ENG 11-. Jude Bellingham 
ENG 12-. Cole Palmer 
ENG 13-. Foto Equipo
ENG 14-. Morgan Rogers
ENG 15-. Anthony Gordon
ENG 16-. Phil Foden
ENG 17-. Bukayo Saka
ENG 18-. Harry Kane
ENG 19-. Marcus Rashford
ENG 20-. Ollie Watkins
CRO 1-. Escudo
CRO 2-. Dominik Livaković 
CRO 3-. Duje Caleta-Car
CRO 4-. Joško Gvardiol
CRO 5-. Josip Stanišić 
CRO 6-. Luka Vušković 
CRO 7-. JJosip Šutalo
CRO 8-. Kristijan Jakić
CRO 9-. Luka Modrić
CRO 10-. Mateo Kovacic
CRO 11-. Martin Baturina 
CRO 12-. Lovro Majer 
CRO 13-. Foto Equipo
CRO 14-. Mario Pašalić 
CRO 15-. Petar Sučić 
CRO 16-. Ivan Perišić 
CRO 17-. Marco Pašalić 
CRO 18-. Ante Budimir 
CRO 19-. Andrej Kramarić 
CRO 20-. Franjo Ivanović
GHA 1-. Escudo
GHA 2-. Lawrence Ati Zigi
GHA 3-. Tariq Lamptey 
GHA 4-. Mohammed Salisu
GHA 5-. Alidu Seidu 
GHA 6-. Alexanderr Djiku
GHA 7-. Gideon Mensah 
GHA 8-. Caleb Yirenkyi 
GHA 9-. Abdul Issahaku Fatawu 
GHA 10-. Thomas Partey 
GHA 11-. Salis Abdul Samed 
GHA 12-. Kamaldeen Sulemana 
GHA 13-. Foto Equipo
GHA 14-. Mohammed Kudus
GHA 15-. Iñaki Williams
GHA 16-. Jordan Ayew
GHA 17-. André Ayew
GHA 18-. Joseph Paintsil
GHA 19-. Osman Bukari
GHA 20-. Antoine Semenyo 
PAN 1-. Escudo
PAN 2-. Orlando Mosquera
PAN 3-. Luis Mejía
PAN 4-. Fidel Escobar
PAN 5-. Andrés Andrade
PAN 6-. Michael Amir Murillo
PAN 7-. Eric Davies 
PAN 8-. José Córdoba 
PAN 9-. César Blackman 
PAN 10-. Cristian Martín
PAN 11-. Anibal Godoy 
PAN 12-. Adalberto Carrasquilla 
PAN 13-. Foto Equipo
PAN 14-. Édgar Bárcenas 
PAN 15-. Carlos Harvey
PAN 16-. Ismael Díaz 
PAN 17-. José Fajardo
PAN 18-. Cecilio Waterman
PAN 19-. José Luis Rodríguez 
PAN 20-. Alberto Quintero  
FWC 9-.  Italia - Mundial Italia 1934
FWC 10-. Uruguay - Mundial Brasil 1950
FWC 11-. Alemania - Mundial Suiza 1964
FWC 12-. Brasil - Mundial Chile 1962
FWC 13-. Alemania - Mundial Alemania 1974
FWC 14-. Argentina - Mundial México 1986
FWC 15-. Brasil - Mundial USA 1994
FWC 16-. Brasil - Mundial Corea - Japón 2002
FWC 17-. Italia - Mundial Alemania 2006
FWC 18-. Alemania - Mundial Brasil 2014
FWC 19-. Argentina - Mundial Catar 2022 
CC 1-. Lamine Yamal - España
CC 2-. Joshua Kimmich - Alemania
CC 3-. Eduardo Camavinga - Francia
CC 4-. Joško Gvardiol - Croacia
CC 5-. Federico Valverde - Uruguay
CC 6-. Virgil van Dijk - Paises Bajos
CC 7-. Alphonso Davies - Canadá
CC 8-. Raúl Jiménez - México
CC 9-. William Saliba - Francia
CC 10-. Lautaro Martínez - Argentina
CC 11-. Harry Kane - Inglaterra
CC 12-. Antonee Robinson - Estados Unidos
"""

def import_all():
    user_id = 'MarcosDB12'
    # Asegurar que el album está inicializado con los nuevos tamaños
    database.repair_user_collection(user_id)
    
    # Procesar línea por línea
    lines = DATA.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line: continue
        
        # Especial para el 00
        if line.startswith('00-.'):
            id_cromo = 'FWC 0'
            nombre = line.split('-. ')[1]
        else:
            # Formato esperado: EQUIPO NUMERO-. Nombre
            match = re.match(r'^([A-Z]+)\s*(\d+)[-.\s]+(.*)$', line)
            if match:
                equipo = match.group(1)
                num = int(match.group(2))
                nombre = match.group(3).strip()
                id_cromo = f"{equipo} {num}"
            else:
                print(f"No se pudo parsear: {line}")
                continue
                
        database.update_cromo_name(user_id, id_cromo, nombre)

if __name__ == '__main__':
    import_all()
    print("Importación completada.")
