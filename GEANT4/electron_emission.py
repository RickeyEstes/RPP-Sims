#----------imports----------#
from Geant4 import *
import g4py.ezgeom
from g4py.ezgeom import G4EzVolume
import g4py.NISTmaterials
import g4py.EMSTDpl
import g4py.ParticleGun, g4py.MedicalBeam

import scipy.stats as ss
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from matplotlib.backends.backend_pdf import PdfPages
import random
import time
import thread
import numpy as np
from scipy import optimize, stats
#----file imports--------#
from geom_constructor import GeomConstructor 
# from beam import BeamInitializer
from beam3 import MyPrimaryGeneratorAction, MyRunAction, MyEventAction, MySteppingAction, Plotter, WipeData
from visualizer import Visualizer

#----------code starts here!----------#
positions_LIST = [
[-0.9089054612575511, 4.803265572358072, 0.0], \
[3.4746695337667517, -10.611447949307724, 0.0], \
[6.5803674694797705, -7.038840078539383, 0.0], \
[8.725291444663059, 16.240961207655616, 0.0], \
[39.34380735750549, -23.019940807136834, 0.0], \
[2.4230180650183044, 4.356736413020018, 0.0], \
[21.740838533678712, 3.3689434097883746, 0.0], \
[-14.240355705810039, 12.655799315917577, 0.0], \
[9.641049758519962, 15.522247326281212, 0.0], \
[-32.62532692443243, 42.404792360306224, 0.0], \
[15.727532867717084, 39.60274347458292, 0.0], \
[20.96783864577733, 23.654995597150936, 0.0], \
[34.07584551269503, 34.27805199626811, 0.0], \
[-2.8069559195885745, 20.795796787067157, 0.0], \
[17.773995257964955, 27.710087788852462, 0.0], \
[-5.99483051873232, -26.405822333770203, 0.0], \
[1.7211798494031392, 0.11343972151169489, 0.0], \
[2.616700319299217, -34.60710570247665, 0.0], \
[-20.10670041669235, -6.668357996894992, 0.0], \
[36.871210224572195, -20.24618268509587, 0.0], \
[-31.496960483876048, 12.79180913254408, 0.0], \
[-52.157591190082734, -19.495463634882103, 0.0], \
[-7.915191204541363, -11.912934155390472, 0.0], \
[-6.479872384266271, 22.12956979735133, 0.0], \
[3.841391064220449, -8.468723694207188, 0.0], \
[6.388200143618688, 16.09749704465041, 0.0], \
[19.28060201090275, 32.4382737469408, 0.0], \
[-0.39641057009744585, -7.772620666608623, 0.0], \
[-33.96418594086262, -16.586833928567064, 0.0], \
[-22.73640827194142, 11.77916132117203, 0.0], \
[-18.6151409591266, -38.929190801368364, 0.0], \
[-43.15163865075342, 1.6310457015008817, 0.0], \
[0.8848420293160879, 1.2529482328264776, 0.0], \
[-21.116347868450585, -15.934382692292003, 0.0], \
[2.801784021635483, 3.787374546549155, 0.0], \
[51.93432989379794, -5.857735238475406, 0.0], \
[-1.9802192901061404, -32.179550403979, 0.0], \
[9.768595417225235, 21.57096279352714, 0.0], \
[-21.00737991909668, 18.614613066914195, 0.0], \
[-13.599886578743039, 13.610855962635988, 0.0], \
[16.45614399830873, 48.72360299398047, 0.0], \
[-7.343127448595921, -21.577672077998447, 0.0], \
[-5.878410794404427, 5.0333024720994715, 0.0], \
[-11.494676266755597, 36.023455758034764, 0.0], \
[-12.823647627951857, -2.9270970893624204, 0.0], \
[-22.095263540545435, 28.221424512019777, 0.0], \
[15.889077206430368, 26.68478701831773, 0.0], \
[-40.648994899650326, 25.522507251550035, 0.0], \
[49.61052433532225, -20.84749099702924, 0.0], \
[1.8593084178486787, 5.817643502389416, 0.0], \
[-0.6647493627913422, 5.182098710842824, 0.0], \
[38.55531772574528, 14.153882676255122, 0.0], \
[-4.993715541782675, 1.991750465556371, 0.0], \
[-8.226068700304234, 20.834403004114158, 0.0], \
[4.828068122856482, 17.065780461268968, -145.21252942187203], \
[1.1146852134869434, 0.9397223873619795, 0.0], \
[-4.002592831604863, 3.6152239731227858, 0.0], \
[7.33203939190821, 7.640437823357874, 0.0], \
[34.76613212595543, 41.26319784318901, 0.0], \
[-1.5381412638800258, -0.9427898961587502, 0.0], \
[-0.614869707409627, 33.88539412887111, 0.0], \
[4.02560641870731, 28.402899402066236, 0.0], \
[23.24272509793514, 23.28616191131644, 0.0], \
[13.781289838179573, -15.428519477958613, 0.0], \
[-9.203503737778803, 10.049292626544776, 0.0], \
[-1.3349276768334173, 14.9994829179441, 0.0], \
[-35.78017269318529, -5.775165267612635, 0.0], \
[0.3305005615826962, 0.008896457349483012, 0.0], \
[31.54906731016675, 36.373988019570746, 0.0], \
[-32.74195513154537, 46.44113726325229, 0.0], \
[0.07418050610561532, 0.035042061687296365, 0.0], \
[-3.350497956562764, 6.9843490130592984, 0.0], \
[5.084127650616492, 32.34067340379708, 0.0], \
[-47.66868883648631, -4.095584368482631, 0.0], \
[-0.7161749778271248, 20.91565808455683, 0.0], \
[15.7523021629113, 28.51572436184776, 0.0], \
[9.59489611284031, 16.119785164546904, -101.65660881652991], \
[13.407299824163719, -32.193590333992304, 0.0], \
[-31.240716701285155, 6.458720943194077, 0.0], \
[-15.097077470193941, -27.585841887789243, 0.0], \
[35.56520184414059, 27.289804651150803, 0.0], \
[-25.297863696496293, 7.4588275360897445, 0.0], \
[-20.69363805654912, 13.175261954391074, 0.0], \
[34.90168192367992, -10.223191330777757, 0.0], \
[32.25519386409043, -46.42689646332159, 0.0], \
[-2.2465000559606, -2.354751581481026, 0.0], \
[-8.231426630354433, -47.05566987135857, 0.0], \
[-26.49345724921921, 11.397581072966853, 0.0], \
[-36.06602625141233, 22.136489076021096, 0.0], \
[49.14602817604363, 24.322474530625136, 0.0], \
[-43.39948917262155, -11.441586385124708, 0.0], \
[16.03701692716757, 44.15757847574473, 0.0], \
[40.81227461566603, -0.681312701396153, 0.0], \
[-20.574873332990805, 3.284956900577816, -24.653340560609934], \
[-6.927150302701371, -1.6679590902621755, 0.0], \
[28.260647640549227, -30.24870436925313, 0.0], \
[-5.952313085289919, 29.090313549206765, 0.0], \
[-28.674047834304123, -0.03518969012908932, 0.0], \
[-16.55850083434155, -30.30621796931937, 0.0], \
[31.717866474510593, 25.105757929367282, 0.0], \
[-47.84800705923241, -15.389439055892938, 0.0], \
[4.160337690197597, -7.315774222210155, 0.0], \
[-20.00319600536602, 29.21094051037866, 0.0], \
[-10.283365336409092, 26.29004269104809, 0.0], \
[19.67162274888036, -18.94858958045316, 0.0], \
[3.161217083462855, 11.064033172537059, 0.0], \
[-36.537890886763606, 30.142924598923933, 0.0], \
[-38.27787281101933, 25.59810473888779, 0.0], \
[10.114546841688062, 21.149576800986885, 0.0], \
[53.48135799663532, 18.188455839809574, 0.0], \
[2.351862294354103, -17.912243701409658, 0.0], \
[-23.361559049816538, -15.568848199715045, 0.0], \
[44.67411882076634, -32.128438329704295, 0.0], \
[-32.328294905990724, -31.163260267032747, 0.0], \
[-32.93740394350477, -25.175809204822002, 0.0], \
[-15.848906592276622, -38.71865025809262, 0.0], \
[-21.395010189690257, -3.975721479769887, 0.0], \
[2.7085998016469324, -2.8787289059526406, 0.0], \
[-12.482021294096633, 16.001079575837437, 0.0], \
[-27.15654358538754, -47.33532372502794, 0.0], \
[17.234261793631934, 6.493743812701338, 0.0], \
[36.08343950431865, 1.5870497700557418, 0.0], \
[-1.9735760724175146, -28.715451549109712, 0.0], \
[17.993068002696038, 23.809984389551587, 0.0], \
[2.22162060988909, 7.899884003821955, 0.0], \
[5.865291728709357, -34.50998130906672, 0.0], \
[17.411312017556373, 16.090042961686578, 0.0], \
[24.867646488642585, -10.279504654427091, 0.0], \
[24.75962181031055, 7.566682347129662, 0.0], \
[17.33091671378586, 42.907800079347815, 0.0], \
[-13.912203449392068, 14.722757964950683, 0.0], \
[38.17962581678516, 6.376804138046227, 0.0], \
[6.340365760562712, 23.755089151078856, 0.0], \
[4.174285519388463, 1.046277222600347, 0.0], \
[14.371163180492672, 2.9045480808312747, 0.0], \
[26.81787476254588, 7.866095655356137, 0.0], \
[24.922929322315575, -0.5865449558676701, 0.0], \
[2.0979492269307656, 0.6974588751580604, 0.0], \
[-10.474539123232985, 3.2268494854454532, 0.0], \
[-42.61096490521265, -22.285421362855132, 0.0], \
[3.2007411308895204, 2.04539265682717, 0.0], \
[-0.11574560653656203, -0.3926955391300225, 0.0], \
[33.24200322949911, -6.331533026093485, 0.0], \
[17.167963072882362, 43.55957668668803, 0.0], \
[39.93640740015996, -22.366791545398048, 0.0], \
[-15.833755854242177, 14.423805014236365, 0.0], \
[-2.6854591117586475, -36.52024553460438, 0.0], \
[-32.90052718209059, -3.54556166286806, 0.0], \
[26.767012157588724, 21.56829417282545, 0.0], \
[10.74525965903389, -12.63595619088223, 0.0], \
[-13.195998513847945, 26.157467527844076, 0.0], \
[-15.395967739619234, 29.59893809566214, 0.0], \
[11.293550335575738, -8.436327783758555, 0.0], \
[-38.239016746326016, 34.46968333193949, 0.0], \
[2.4895875633398803, 7.834389975491559, 0.0], \
[30.9251277131313, 0.4442677733416807, 0.0], \
[-50.3625150082051, -25.095209602739168, 0.0], \
[30.461307165890222, -31.18542724362083, 0.0], \
[-24.33671811982883, -26.278056433165876, 0.0], \
[24.84755613073156, -18.800509957923012, 0.0], \
[-0.48539614735518877, -1.6866392385105078, 0.0], \
[-11.146249842419572, -1.0714998829212228, 0.0], \
[3.5346273390540057, -3.5709830696158895, 0.0], \
[45.68834328151655, 29.92098031701235, 0.0], \
[-14.382966739605386, 4.643354824278576, 0.0], \
[2.545256897916564, 10.867828947568718, 0.0], \
[-31.72606899592656, -0.785276972809479, 0.0], \
[9.438291002244418, 39.70210672641772, 0.0], \
[-46.62911648858608, 11.33687895536628, 0.0], \
[-35.43139826715538, 20.846178026530936, 0.0], \
[11.922333109144155, 18.58172930690357, 0.0], \
[-1.380935451979498, 3.215413113123941, 0.0], \
[1.4883156033156193, 1.8870696121580561, 0.0], \
[20.888756464906866, -6.684125585191567, 0.0], \
[-29.883361274569886, 6.356644536561271, 0.0], \
[-35.97392113552532, -3.3807541293384302, 0.0], \
[11.071709700476667, 4.387950221806053, 0.0], \
[-21.264218370420025, -26.942727887947893, 0.0], \
[-29.729400314996365, -26.957002649177348, 0.0], \
[1.8003851084471667, -4.672440657468006, 0.0], \
[2.6628266611482254, -2.7422954037097496, 0.0], \
[17.955627154757664, 0.8300338956830324, -134.61600157665464], \
[12.564633589069802, -3.3603069088678144, 0.0], \
[0.3912193381507788, -19.18272567608081, 0.0], \
[18.663294200897024, 1.08220829341733, 0.0], \
[12.168327931255353, 11.589281576239962, 0.0], \
[28.11771005957558, -43.935294226512944, 0.0], \
[-12.662113184882013, 30.170678014254516, 0.0], \
[46.81430457655962, -17.712296190113054, 0.0], \
[20.286367375460742, 6.528607039405988, 0.0], \
[9.831968813293841, -33.659082832146936, 0.0], \
[-0.7495984676300887, 26.343621726598368, 0.0], \
[8.702726568580431, -16.460697328982086, 0.0], \
[13.040125497271466, 9.815975133384951, 0.0], \
[8.170812691078634, -2.5446305780111973, 0.0], \
[7.804048944912892, -21.114491023003037, 0.0], \
[-10.133879775771629, -10.9917159915002, 0.0], \
[-18.149440502605575, -9.26466272590784, -40.704340257254046], \
[-6.716058662082492, 2.699611690125899, 0.0], \
[4.874324152493348, 9.117435098481199, 0.0], \
[1.1200809961764786, 3.390598885877616, 0.0], \
[-6.035694409238041, -16.84198620673931, -138.28806160408078], \
[-39.049027814794684, -32.79995118825045, 0.0], \
[3.140654184790244, 32.95668119824078, 0.0], \
[34.5633537631739, -40.31090058055801, 0.0], \
[-44.794922761874716, 25.07937514115295, 0.0], \
[-12.737673607811184, -27.884042776924037, 0.0], \
[-38.05385622758545, -35.89174679448037, 0.0], \
[15.883483816433285, 10.457260312812082, 0.0], \
[-18.197394872361564, -47.91770926238625, 0.0], \
[16.71721027722034, -52.05853546080506, 0.0], \
[-4.214940762396955, -28.39713354061325, 0.0], \
[-13.091405920810665, 25.415785603675666, 0.0], \
[12.401591717484438, -15.059672557581306, 0.0], \
[23.259209849158523, -25.88762338662142, 0.0], \
[-5.404034593057702, 52.65831265163167, 0.0], \
[-24.303313113192292, 28.46864226457885, 0.0], \
[2.0418625779156816, 2.142687617511136, 0.0], \
[-3.63561405367223, 37.908550303149454, 0.0], \
[-6.290673785505976, -14.371546111335707, 0.0], \
[-5.1111070942744306, 27.08848515436149, 0.0], \
[-1.2931258646676635, -2.961204078643165, 0.0], \
[-50.626572443286804, 8.185700575624411, 0.0], \
[-1.0293332008073994, -1.2603140096657834, 0.0], \
[5.024067639283111, -2.523258426425916, 0.0], \
[-18.47772439264735, 43.32667172397283, 0.0], \
[-3.4964408003454492, 22.421965510254257, 0.0], \
[-12.977521721325473, -18.879074721857254, 0.0], \
[38.88471258034482, -14.814098386369073, 0.0], \
[29.000092864379077, -16.245063766504906, 0.0], \
[10.883554344331822, 5.667687381679492, 0.0], \
[-5.579418852484342, -48.3886352923472, 0.0], \
[16.94092564929751, 25.95487369153693, 0.0], \
[14.670883888128559, -5.911218755596749, 0.0], \
[-17.144892698278596, -44.717697505112106, 0.0], \
[43.894902275558636, -16.217615566001562, 0.0], \
[-9.84623581587756, -35.746266464943346, 0.0], \
[-1.6683428868835861, 7.022415302453967, 0.0], \
[-28.160040185836678, 18.535970815739866, 0.0], \
]

momenta_LIST = [
[6.083083760523721, -11.36191102741659, 43.380856489556784], \
[-19.683866795247884, 31.724486874586685, 25.575338913318724], \
[16.395595538203523, -28.70055830926834, 30.910484300378226], \
[-7.337329271915162, -44.48112310930159, 3.9482814097595758], \
[2.8908444156378748, -43.47937019614678, 12.214050348307817], \
[-15.918028672727676, -36.73474825037045, 21.099058608291617], \
[18.473260467707068, -14.752348126764582, 38.58889104961423], \
[-12.400290589234093, 31.187153283555567, 30.35769924369371], \
[30.823648750132143, 22.22461995403511, 24.575690949130646], \
[39.093157216400435, 18.613557456782182, 13.16268124877552], \
[41.81417170924983, 13.941255638181971, 10.257293770787227], \
[39.81302049387819, 7.209001511728748, 20.271885367620037], \
[37.01205922620288, -17.014185200521155, 19.713462755143183], \
[20.888222110291277, -30.628196495695953, 25.95363936892429], \
[24.73737927335824, -9.679637427494827, 36.638263140578424], \
[-29.524881210397073, -33.27572168690704, 8.306827055347066], \
[17.728464361530307, -0.18936472639673188, 41.63725894415177], \
[-29.535528710815946, 26.4011586242481, 21.877545727751478], \
[-37.71466561237433, 5.1509766697828026, 24.475846810562892], \
[-28.407789411176253, -22.37193567656198, 27.211939196867906], \
[-23.184885131994616, 38.44855922295566, 5.671422669409006], \
[-13.200297888204556, 42.10142849655982, 10.06069054348275], \
[14.683740507666108, 42.54995358183541, 4.678125146592105], \
[6.535006214979481, 42.60772483270298, 13.77937293024779], \
[10.57754564399282, -41.13049058288265, 15.633103100813038], \
[-0.010278000757524967, -37.175473002493725, 25.806583295809624], \
[12.411043191298793, -37.557423831006645, 21.986394931453635], \
[-4.269199138512586, 37.17324228949711, 25.454265583631884], \
[-34.86575353697061, 16.256342386782993, 23.834978550502292], \
[-25.41188451504349, 35.983916554631755, 10.362891236686359], \
[-25.807046190719028, 25.17634496253505, 27.35221492379604], \
[-22.843523281277154, 35.055867563087986, 17.241091424181498], \
[-23.824377363550198, -35.835975616099056, 14.0063390963346], \
[-23.091637862738, 8.796935276192485, 37.9128715684086], \
[-16.0399507750941, -27.946154145149457, 31.77621890074564], \
[13.003777386645345, -43.08240099660568, 4.775367844076579], \
[-23.235530568909045, 37.7477146309057, 9.1222694174751], \
[32.819275256754715, 27.052816970962798, 15.460786058831383], \
[-11.701431028685747, 40.04169554468096, 17.542370700335432], \
[39.7613935373529, -18.254474211442325, 11.567255302427522], \
[37.0903520730477, -17.350044164824865, 19.268559639370885], \
[-30.020316933868394, -32.23461558582214, 10.37813900583178], \
[-10.42381294725627, 16.983819951659235, 40.63114105572516], \
[34.828247064997505, -10.726322898668352, 26.8316015819592], \
[-44.47403486800362, 0.5237142052737475, 8.353537334015597], \
[43.20434439599438, -9.179009186520927, 9.855255230894512], \
[38.89614700702095, 17.291526624692985, 15.36517149255902], \
[13.201288083863568, 36.55443601945234, 23.18393495993739], \
[-23.719488962875474, -36.218580935843256, 13.175578861431475], \
[-8.64150645643936, -42.911693777929685, 11.485057390910487], \
[5.560814985318048, -10.884723809027456, 43.57287876994419], \
[34.03531544193824, -22.123547558614344, 20.00353934156378], \
[-15.769196696164112, 10.866096260000619, 41.0031221692457], \
[29.577439231261057, -26.650827709763977, 21.515206503901755], \
[25.20128498923522, 37.52846870957068, 2.1224776102757184], \
[34.731649903976084, 27.77233933803969, 8.390786771239718], \
[8.374068930233712, -1.8168223978329545, 44.4361313114275], \
[-15.22021659626397, -27.96013154893826, 32.16475851811853], \
[41.730786321878405, -16.73011777183032, 5.161421538531167], \
[31.25431219978969, 20.82617229470176, 25.247458416036142], \
[27.264358091243754, -24.46145665693582, 26.576071118456944], \
[27.524997921809653, 32.4547368901248, 15.396758840650403], \
[22.132484846429122, -14.676250545986965, 36.643640982222315], \
[-34.373321426659196, 13.910942355714248, 25.94139735780568], \
[-16.587748528182264, 34.075859369874934, 24.732125807748375], \
[15.67433421778974, -41.709596230275324, 7.9133096196489525], \
[29.469917456306206, 33.805185950514186, 6.060446185691034], \
[32.52172206403488, 0.647845833670793, 31.46289131286986], \
[22.687948879138975, -31.98790623229332, 22.583765641087993], \
[35.088851847909254, 28.258094974564663, 4.271789367929919], \
[-15.310266350608005, -7.0728015123802725, 41.99484329105077], \
[-8.47775356572193, 31.840433995964, 31.02112340692305], \
[31.185214024079958, 31.57233067452199, 8.869385663672789], \
[-22.847516631936465, 36.033189157468776, 15.086281944053066], \
[15.146056968911074, 41.55109451815001, 9.596829822304048], \
[15.735713293421744, -24.822827615523824, 34.412355285815856], \
[34.587059831046226, 29.087001465173334, 2.3827039280264], \
[-36.39921019509532, 15.62738111451616, 21.88328349848196], \
[35.074559366566476, 18.524272749106185, 21.78582668520812], \
[-25.54899968170995, 5.144617976661788, 36.99698854147718], \
[8.041284212489359, -38.53939012628042, 22.31700689851416], \
[-31.504566214088626, 31.045733598878332, 9.571853162767542], \
[-23.099159917168063, 37.7178975002796, 9.580431059169445], \
[-34.17304955585691, -19.975478162681327, 21.935783465041506], \
[-37.26237352638382, -24.763030861477375, 6.8046647039930575], \
[-14.412509062936916, -11.384075341618551, 41.360343943530175], \
[-38.77970903031007, -2.330246265901489, 23.20990650271429], \
[-21.634116298240738, 34.14956469068374, 20.34128519614729], \
[8.614383362339082, 34.00044934982072, 28.596459279024934], \
[8.856658130925204, -44.02794223687996, 5.576338327063578], \
[-5.19640760838569, 35.356556643840236, 27.76521007048981], \
[38.73835051596235, -2.2298490372735276, 23.288701393023388], \
[12.749188442878141, -32.51445328284944, 28.77957890180786], \
[-38.923956607466565, 22.909422509195252, 2.842464127344017], \
[29.37191774246048, 12.869593500686902, 31.93211003452815], \
[-15.554060024931589, -31.330864550483465, 28.713129109522082], \
[29.43333801073168, -26.64570323330424, 21.718212466699423], \
[-33.48386224699072, 22.647116117970008, 20.345386223017062], \
[-24.32301063759277, 12.473344723510952, 36.066639224247254], \
[40.964224144633896, -8.395841042189193, 17.304272114783814], \
[6.409631985553194, 43.83764610613339, 9.22892418883054], \
[-27.013197432825987, 34.031325027033745, 12.655106532919845], \
[42.90093166477569, -13.068978734723606, 6.058671234320999], \
[28.196997094496407, -10.769862974482875, 33.718467437945996], \
[-6.049314483208364, -24.179694993858288, 37.772262101802035], \
[13.960191902378991, 15.723388692627072, 40.073479136073516], \
[11.586386290627996, 39.02820456023731, 19.76235161939538], \
[32.550696167838716, 22.064278736655474, 22.396772598305837], \
[6.14726088289028, -30.140392003601136, 33.19282442798358], \
[11.626139897173086, -43.2575016255602, 6.451128909424805], \
[-19.666739515271797, 39.980673737878504, 7.922166642008951], \
[4.713881620089649, 29.835602409647954, 33.698839578317674], \
[-27.855806081049494, -33.597688014142314, 11.968503151159874], \
[-25.134918867595246, 25.1198850801831, 28.02182840354639], \
[-29.583789283700863, 18.67534014537727, 28.705865638786193], \
[-25.10628469492146, 26.04956558197353, 27.186214186753045], \
[-36.53644384401044, 10.72369028932113, 24.455804583210735], \
[10.314656794565186, -15.520359835079148, 41.2398099631896], \
[37.17842120626314, -21.553682389886053, 14.184477855938155], \
[-43.15403520366276, 11.552041469631689, 7.230160684586819], \
[-32.06741372601549, -27.655176521908455, 15.964580435032953], \
[-33.320542002541266, -30.071697721413393, 5.781878311485259], \
[-24.461117336760474, -23.759141403720445, 29.751513884090897], \
[-0.4015291510227823, -39.698332919303986, 21.72272491583374], \
[18.242494666672275, 40.88386948770032, 6.611826075232167], \
[-27.68043034206534, -2.436907438367679, 35.71905511369102], \
[37.10428929937833, 8.747136191564973, 24.387598570467173], \
[3.6615064595372444, -24.551869894124643, 37.839063084975336], \
[41.64416944235685, -8.693904943368857, 15.432913149886483], \
[40.595446652429594, 2.7378959914803875, 19.811846875785655], \
[0.10227510026548581, 23.22697888422579, 38.839318115996775], \
[21.231523860275434, -27.506131778276686, 28.99363290735799], \
[27.25620422842673, 26.680719093391957, 24.356399563929866], \
[18.72848945815543, 1.1878688848676537, 41.18043576904115], \
[-35.138925750929566, -18.937181304216352, 21.322164555267328], \
[43.9362068796907, -10.158039562486357, 3.797314481575294], \
[13.790336902719048, -20.055298293271466, 38.152421397303314], \
[-35.04147575484708, -13.489149080144012, 25.261303885906496], \
[44.56933498672178, -4.655807312238627, 6.316128332505906], \
[-24.683858540817926, 30.028463631386657, 23.173134002015754], \
[-1.8950188730343995, -4.77421690026353, 44.962333085151194], \
[8.899469345759666, 31.241622858419042, 31.50803209558149], \
[-2.011414239524352, -26.873627251232993, 36.355990030788945], \
[40.64550156913188, 2.093732191470906, 19.787751961860064], \
[4.228377354102128, -43.879508790940044, 10.232554579240324], \
[-18.990775970089793, 40.22459541372046, 8.326343246369309], \
[-27.26815311445453, 24.269385036939386, 26.747717952293534], \
[-24.92607382670055, 23.648506215104454, 29.45224333357375], \
[18.117237567377074, -20.332013064282794, 36.14374894336578], \
[14.672954121358744, -37.51387787596275, 20.625446032991732], \
[15.975129275288001, 19.80065583940551, 37.426259671081915], \
[29.148519801485666, 1.168774345149462, 34.59759240051999], \
[18.458693540879427, -27.710293012722442, 30.64982763267947], \
[30.335082577696213, 27.497325438523642, 19.2788873831524], \
[-6.488238897154549, -41.89320295679454, 15.838495573578706], \
[-27.05998928883086, -24.863111557937888, 26.41170769461708], \
[-17.382427609027335, 41.082060563038084, 7.623066988541765], \
[-31.87783595426759, -16.72883154735215, 27.421623036084494], \
[1.525721648589315, 43.35483773060777, 12.885102203851364], \
[8.49312494263752, -37.34222161068833, 24.112672060287927], \
[9.744857536552324, 38.870138950534226, 21.027260628965948], \
[29.544558532440337, 11.740121607089279, 32.206897487556326], \
[10.266920585332777, -16.01916246172144, 41.060594439431156], \
[31.066423316272385, -31.31017363492362, 10.126500347360935], \
[-35.1304889579193, 23.90780423952209, 15.564744842823472], \
[1.6334075928459533, -31.752221834064468, 32.20441007433598], \
[-23.94362117436917, 24.52578578841753, 29.54969503258802], \
[24.19346503186714, -37.84199377740762, 5.536731590249284], \
[-11.821424788331505, 41.95026261313046, 12.18298086115255], \
[5.470613007231108, 34.520953595948086, 28.746683220008407], \
[-2.9361767818685687, -36.924438001257165, 25.999238146471363], \
[4.026144492877391, -2.365239463275508, 45.013236306711356], \
[24.777782888056247, 28.350770668938527, 25.105595345054102], \
[9.979781228642839, -21.41339321335262, 38.59878492541925], \
[22.099883524956777, 20.013863781288205, 34.04461844003225], \
[26.913218568229347, 31.244893364468997, 18.63949958935796], \
[21.060582883962667, -1.7883654859960596, 40.01561242160661], \
[-15.364769222724364, 24.368569787203647, 34.90117925312278], \
[2.257784371958158, 44.91113445642852, 5.088030224589922], \
[-8.024009846515076, 9.814343301774274, 43.442946165493275], \
[-11.868829614160134, 7.887976925921857, 42.95237296827918], \
[43.51711616201155, -12.226141351495155, 2.185797016022813], \
[-31.584644338536346, -2.204926484803353, 32.33487561758629], \
[-16.007747164381318, 40.36697572673854, 12.737933168224101], \
[-26.580097892774923, -16.35770463139129, 32.77071154556553], \
[-19.948648489222652, -37.36088510779753, 15.944006002739334], \
[-42.453676302112825, -10.232164570784715, 11.873660624752691], \
[29.225898565662277, -2.7373643811234336, 34.44342214813412], \
[0.8786774484900937, -42.67673473391474, 15.030631337125866], \
[-19.566512423148183, -24.01049798190918, 32.99459377315507], \
[-33.31566643159495, 15.099483084167536, 26.647094040619812], \
[19.740541532733868, 39.38276863319321, 10.358773806719686], \
[3.351724761443798, -37.859971582230735, 24.563878621182887], \
[-25.363231146599976, -35.25652698311179, 12.71532346789698], \
[33.48206187537066, -17.51856648079477, 24.900742981522153], \
[-5.03228528038047, -37.76059755923196, 24.42967492265485], \
[15.237378351522665, 33.978328119900866, 25.715582030140844], \
[-44.91306020540826, -4.823744246472403, 2.746662416460642], \
[31.404280630929, -6.452362836161096, 31.939533682951367], \
[25.775332198286993, 30.863063944351694, 20.762927877224083], \
[-1.7822060594499485, -14.387013938583271, 42.86995698029881], \
[-27.808966431662274, -35.63670517077969, 2.1638554881517424], \
[-30.718906620566294, 26.894224252014684, 19.520376992242582], \
[23.05160005035491, -34.23068575890218, 18.570932329685803], \
[-31.47507755350177, -27.839069377613686, 16.801825769524594], \
[16.07505519732402, 37.554071397834676, 19.47511134369511], \
[-36.175117232834175, -20.813932214193418, 17.49676424295832], \
[-16.44865388038856, 41.38165142535944, 8.062031433405915], \
[43.3190173098409, 10.504792573887105, 7.817142207310194], \
[-41.72071550564839, 4.37691907166798, 16.97704677312337], \
[-40.993914723419444, -13.841940958406932, 13.262551268628204], \
[-28.191748226585656, -35.21929237197158, 3.580840229106686], \
[4.769922397630896, 40.14005675515212, 20.347464805565966], \
[11.75906263602769, -38.56171871006017, 20.560008172376126], \
[-25.4320049196007, -12.895956906718293, 35.14118753299995], \
[42.0457115820343, 0.5742040927853906, 16.727942707344948], \
[36.3346630730529, 3.054270168215683, 26.80409172322901], \
[-29.363850637775606, -34.20901912808148, 3.937375523995812], \
[28.352395119818787, 20.004341892556635, 29.051052242825556], \
[0.2197708808072407, 31.45694785846829, 32.53317955856077], \
[25.326391960321324, -16.588137183552927, 33.636337717590486], \
[3.497112061394153, 14.383489454649926, 42.7654191881481], \
[-12.33482169426929, 43.09978939813761, 6.185140872022908], \
[-24.78619167214352, -28.320359900895784, 25.13160475328819], \
[14.728739137895285, -12.372004212977378, 40.963317677672315], \
[41.06652500704578, -1.287538383479701, 18.970461479804598], \
[12.173353169983274, 38.4717148808686, 20.48736846752191], \
[-37.09210607165656, -21.96042401270833, 13.780823065080014], \
[-25.77652368135685, -25.412886352994356, 27.16158452878335], \
[-44.70003234212502, -5.106904532375485, 4.880806768371376], \
[40.36890557565355, 10.0758335270312, 17.799569695909], \
[-38.91161366018243, -0.9984071566650299, 23.084305177115994], \
[25.12882129870812, -6.3686560614265835, 37.09418013797916], \
[-37.185823444569124, 1.4905878884178343, 25.748559619835735], \
[-31.744158671113173, 23.05632983425441, 22.554593430990053], \
[-1.9777522756129142, -38.74210934928395, 23.305216135115177], \
[-34.88391856635013, -16.169437412438572, 23.86749168265245], \
[12.847245232960606, -29.375088965803023, 31.93819152950475], \
[24.28982675086469, 15.947024167868896, 34.694270083147494], \
]


spherical_coor_LIST = []
# spherical_coor_LIST = [[0,0]]
pi = np.pi
step = 6
for phi in np.arange(0, pi, pi/step): # smaller steps means more clusters, range goes to pi since clusters are double sided
	for theta in np.arange(0, pi, pi/step):
		sph_coor = [theta, phi] # phi, theta
		spherical_coor_LIST.append(sph_coor)

cluster_coor_LIST = []
global cluster_width
cluster_width = 160
spacing = 40./7
interval = cluster_width + spacing
interval *= 3
global edge
edge = 500
for x in np.arange(-(edge-cluster_width/2 - spacing), edge - (cluster_width/2 + spacing) + interval, interval):
	for y in np.arange(-(edge-cluster_width/2 - spacing), edge - (cluster_width/2 + spacing) + interval, interval):
		for z in np.arange(-(edge-cluster_width/2 - spacing), edge - (cluster_width/2 + spacing) + interval, interval):
			cluster_coor = [x,y,z]
			# cluster_coor_LIST.append(cluster_coor)
			# print cluster_coor
			# time.sleep(1)
			opposite = np.multiply(cluster_coor, -1)
			for i in cluster_coor:
				if np.abs(i) == edge-cluster_width/2 - spacing and cluster_coor not in cluster_coor_LIST:
					cluster_coor_LIST.append(cluster_coor)
					break

energy_LIST = [.002] 

class SEEConstructor(object):
	def __init__(self):
		# from EZsim.EZgeom import G4EzVolume
		g4py.NISTmaterials.Construct()
		# set DetectorConstruction to the RunManager
		# G4VUserDetectorConstruction.Construct()
		g4py.ezgeom.Construct()
		exN03PL = g4py.EMSTDpl.PhysicsListEMstd()
		gRunManager.SetUserInitialization(exN03PL)
		# reset world material
		air= gNistManager.FindOrBuildMaterial("G4_AIR")
		# g4py.ezgeom.SetWorldMaterial(air)




	def construct(self):

		NaI= gNistManager.FindOrBuildMaterial("G4_SODIUM_IODIDE")
		GRAPHITE = gNistManager.FindOrBuildMaterial("G4_GRAPHITE")
		scale_factor = 5

		GC.ConstructSphere("Sphere", GRAPHITE , [0., 0., 0.], m, (.10-30e-9)*scale_factor, .10*scale_factor, 0., 360., 0., 90)


GC = GeomConstructor()
SEEConstructor = SEEConstructor()
VIS = Visualizer()
# # CC = ClusterClass()

viz_theta = 90
viz_phi = 45


class SecondaryElectronEmissionProcess(object):

	# def __init__(self):

	def runSEE(self, energy, positions, momenta):
		
		SEEConstructor
		SEEConstructor.construct()
		# viz_theta += .1
		PGA_1 = MyPrimaryGeneratorAction(energy, positions, momenta)
		gRunManager.SetUserAction(PGA_1)

		myEA = MyEventAction()
		gRunManager.SetUserAction(myEA)

		mySA = MySteppingAction()
		gRunManager.SetUserAction(mySA)

		myRA = MyRunAction()
		gRunManager.SetUserAction(myRA)

		# gRunManager.Initialize()

		gRunManager.BeamOn(1)

		# VIS.visualizer(viz_theta, viz_phi)