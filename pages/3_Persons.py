import streamlit as st

st.header("👤 :violet[Historical Figures]", text_alignment="center")

persons = [
    {
        "name": "Clistenes de Atenas",
        "desc": "Considerado el 'padre de la democracia ateniense', reformó la estructura política de la ciudad para reducir el poder de la aristocracia. Introdujo el sistema de tribus basadas en la residencia y no en el linaje, fomentando la participación ciudadana. Su mayor innovación fue la creación del ostracismo para proteger al Estado de posibles tiranos. Gracias a él, Atenas entró en su época de mayor esplendor político.",
        "image": "images/persons/clistenes.svg"
    },
    {
        "name": "Platón",
        "desc": "Fue el filósofo griego que fundó la Academia, la primera institución de enseñanza superior en Occidente. Discípulo de Sócrates y maestro de Aristóteles, desarrolló la Teoría de las Ideas, donde distinguía entre el mundo sensible y el inteligible. Su obra, escrita mayormente en forma de diálogos, aborda temas como la justicia, la ética y la política ideal. Es una de las figuras más influyentes de la historia del pensamiento universal.",
        "image": "images/persons/Platon.svg",
    },
    {
        "name": "Aristóteles",
        "desc": "Polímata griego que sentó las bases de la lógica, la biología y muchas otras ciencias. A diferencia de Platón, se centró en la observación empírica y el estudio del mundo físico como base del conocimiento. Fue tutor de Alejandro Magno y fundó el Liceo en Atenas para enseñar su propio sistema filosófico. Sus escritos dominaron el pensamiento científico y teológico europeo durante casi dos milenios.",
        "image": "images/persons/Aristotle.svg"
    },
    {
        "name": "Qin Shi Huang",
        "desc": "Fue el primer emperador de una China unificada tras conquistar los Reinos Combatientes. Estandarizó la escritura, la moneda y los sistemas de pesos y medidas para consolidar su poder. Es famoso por iniciar la construcción de la Gran Muralla y por el impresionante mausoleo que alberga a los Guerreros de Terracota. Su gobierno fue autoritario y centralizado, dejando una huella imborrable en la identidad china.",
        "image": "images/persons/qin.svg"
    },
    {
        "name": "Julio César",
        "desc": "Brillante general y estadista romano que expandió el dominio de la República mediante la conquista de las Galias. Al cruzar el Rubicón, desafió al Senado y se convirtió en dictador perpetuo tras una guerra civil. Introdujo reformas sociales y el calendario juliano, que influyó en la medición del tiempo actual. Su asesinato a manos de un grupo de senadores marcó el principio del fin de la República Romana.",
        "image": "images/persons/julio.svg"
    },
    {
        "name": "Augusto",
        "desc": "Nacido como Octavio, fue el primer emperador de Roma y el artífice de la transición del sistema republicano al imperial. Inició el periodo de estabilidad conocido como la 'Paz Romana', que duró dos siglos. Profesionalizó el ejército, reformó el sistema tributario y embelleció la ciudad de Roma con grandes obras públicas. Su hábil diplomacia y gestión administrativa consolidaron el Imperio más poderoso de la Antigüedad.",
        "image": "images/persons/augusto.svg"
    },
    {
        "name": "Mahoma",
        "desc": "Profeta y fundador del Islam, nació en La Meca y unificó a las tribus de Arabia bajo una sola fe monoteísta. Tras la Hégira a Medina, se convirtió en un líder tanto religioso como político y militar. Según la tradición, recibió las revelaciones de Alá que conforman el Corán, el libro sagrado de los musulmanes. Su legado transformó radicalmente la historia, la cultura y la geopolítica de Oriente Próximo y el mundo.",
        "image": "images/persons/mahoma.svg"
    },
    {
        "name": "Carlomagno",
        "desc": "Rey de los francos y primer Emperador del Sacro Imperio Romano Germánico en el año 800. Unificó gran parte de Europa Occidental mediante campañas militares y promovió el llamado 'Renacimiento carolingio'. Impulsó la educación y la cultura, estableciendo escuelas y protegiendo a los intelectuales de su época. Es considerado a menudo como el 'Padre de Europa' por sentar las bases de las futuras naciones del continente.",
        "image": "images/persons/carlomagno.svg"
    },
    {
        "name": "Leif Erikson",
        "desc": "Explorador nórdico que, según las sagas islandesas, llegó a América del Norte casi 500 años antes que Cristóbal Colón. Estableció un asentamiento en una región que llamó Vinlandia, ubicada probablemente en la actual Terranova, Canadá. Su expedición demuestra el avanzado conocimiento náutico de los vikingos y su capacidad de exploración transoceánica. Aunque sus asentamientos no fueron permanentes, su hazaña es un hito clave en la historia de la navegación.",
        "image": "images/persons/leif.svg"
    },
    {
        "name": "Johannes Gutenberg",
        "desc": "Orfebre alemán que revolucionó el mundo con la invención de la imprenta de tipos móviles a mediados del siglo XV. Su innovación permitió la producción masiva de libros, siendo la Biblia de 42 líneas su obra más famosa. Facilitó la difusión del conocimiento, las ideas religiosas de la Reforma y los avances científicos del Renacimiento. Se le considera el motor de una revolución cultural que puso fin al monopolio del saber por parte de la élite.",
        "image": "images/persons/Gutenberg.svg"
    },
    {
        "name": "Cristóbal Colón",
        "desc": "Navegante genovés que, bajo el patrocinio de los Reyes Católicos, realizó un viaje a través del Atlántico buscando una ruta hacia Asia. En 1492 desembarcó en tierras americanas, iniciando un proceso de contacto permanente entre Europa y el 'Nuevo Mundo'. Su llegada cambió drásticamente la geografía política, la economía global y la demografía del planeta. A pesar de la controversia por el impacto de la colonización, su viaje es uno de los eventos más trascendentales de la historia.",
        "image": "images/persons/cristobal_colon.svg"
    },
    {
        "name": "Nicolás Copérnico",
        "desc": "Astrónomo polaco que desafió la visión tradicional del universo al proponer el modelo heliocéntrico. En su obra De revolutionibus orbium coelestium, planteó que la Tierra y los planetas giran alrededor del Sol. Su teoría supuso una ruptura con el sistema geocéntrico de Ptolomeo, que la Iglesia había defendido durante siglos. Marcó el inicio de la Revolución Científica y cambió para siempre nuestra comprensión del cosmos.",
        "image": "images/persons/copernico.svg"
    },
    {
        "name": "Isaac Newton",
        "desc": "Físico y matemático inglés que formuló las leyes del movimiento y la ley de la gravitación universal. En su obra Principia, estableció las bases de la mecánica clásica que rigieron la ciencia durante siglos. También desarrolló de forma independiente el cálculo infinitesimal y realizó importantes descubrimientos sobre la naturaleza de la luz. Es considerado uno de los científicos más grandes de todos los tiempos por unificar la física terrestre y celeste.",
        "image": "images/persons/newton.svg"
    },
    {
        "name": "Charles Darwin",
        "desc": "Naturalista inglés que revolucionó la biología con su teoría de la evolución mediante la selección natural. En El origen de las especies, explicó cómo las poblaciones cambian a lo largo del tiempo para adaptarse a su entorno. Su trabajo unificó las ciencias de la vida, ofreciendo una explicación científica para la diversidad biológica. Aunque causó una gran controversia religiosa en su época, su legado es el pilar fundamental de la biología moderna.",
        "image": "images/persons/darwin.svg"
    },
    {
        "name": "Alexander Graham Bell",
        "desc": "Científico e inventor a quien se le atribuye históricamente la patente del primer teléfono capaz de transmitir voz humana de forma clara. Su interés por la comunicación nació de su trabajo con personas sordas y su estudio de la acústica. Fundó la Bell Telephone Company, que impulsó la expansión global de las telecomunicaciones. Además del teléfono, investigó en áreas como la aviación y los barcos de alta velocidad.",
        "image": "images/persons/bell.svg"
    },
    {
        "name": "Adolf Hitler",
        "desc": "Líder del Partido Nazi que se convirtió en dictador de Alemania en 1933. Su política expansionista y su ideología racista desencadenaron la Segunda Guerra Mundial, el conflicto más mortífero de la historia. Fue el principal responsable del Holocausto, el genocidio sistemático de seis millones de judíos y otros grupos minoritarios. Su régimen totalitario terminó en 1945 con la derrota de Alemania y su posterior suicidio en Berlín.",
        "image": "images/persons/Hitler.svg"
    },
    {
        "name": "Watson y Crick",
        "desc": "James Watson y Francis Crick fueron los científicos que descubrieron la estructura de doble hélice del ADN en 1953. Su hallazgo, basado en parte en las imágenes de difracción de rayos X de Rosalind Franklin, permitió entender cómo se almacena y transmite la información genética. Este descubrimiento dio paso a la era de la biotecnología y la medicina genómica. Por su investigación, compartieron el Premio Nobel de Medicina en 1962 junto a Maurice Wilkins.",
        "image": "images/persons/watson.svg"
    },
    {
        "name": "Tim Berners-Lee",
        "desc": "Científico de la computación británico conocido como el inventor de la World Wide Web (WWW). En 1989, mientras trabajaba en el CERN, desarrolló el primer servidor web, el primer navegador y los protocolos HTTP y HTML. A diferencia de otros inventores, decidió que su tecnología fuera gratuita y abierta para todo el mundo. Su contribución ha transformado radicalmente la comunicación, la economía y el acceso a la información en la sociedad moderna.",
        "image": "images/persons/tim.svg"
    },
    {
        "name": "Neil Armstrong",
        "desc": "Fue un astronauta y amartizaje estadounidense que hizo historia al convertirse en el primer ser humano en pisar la Luna. Como comandante de la misión Apolo 11 en 1969, pronunció la icónica frase: 'Es un pequeño paso para un hombre, pero un gran salto para la humanidad'. Antes de su carrera espacial, destacó como piloto de pruebas y sirvió en la Marina durante la Guerra de Corea. Su calma bajo presión fue decisiva para aterrizar manualmente el módulo Eagle cuando el combustible se agotaba. Tras su hazaña, mantuvo un perfil bajo, dedicándose a la docencia universitaria y a la ingeniería aeroespacial.",
        "image": "images/persons/neil.svg"
    },
]

for p in persons:
    with st.container(border=True):
        col1, col2 = st.columns([1, 3], vertical_alignment="center")
        with col1:
            st.image(p['image'])
        with col2:
            st.subheader(p['name'])
            st.write(p['desc'])
