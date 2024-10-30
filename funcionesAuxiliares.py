def generarArch2Class(subject, class_id):
    xml_template = f"""
<map>
    <type>Arch2Class</type>
    <class><id>{class_id}</id></class>
    <arch>
        <nodepath>{subject}</nodepath>
    </arch>
</map>"""
    return xml_template

def dividir_cadenas(cadena1, cadena2):
    segmentos1 = cadena1.split('/')
    segmentos2 = cadena2.split('/')
    
    comun = []
    resto1 = []
    resto2 = []
    
    for seg1, seg2 in zip(segmentos1, segmentos2):
        if seg1 == seg2:
            comun.append(seg1)
        else:
            resto1 = segmentos1[segmentos1.index(seg1):]
            resto2 = segmentos2[segmentos2.index(seg2):]
            break
    comun = "/".join(comun)
    resto1 = "/".join(resto1)
    resto2 = "/".join(resto2)
    
    return comun, resto1, resto2

def generarArch2ClassLabel(subject, class_id, label_id):
    
    nodepath, infopath, valuepath = dividir_cadenas(subject, label_id)
    
    xml_template = f"""
<map>
    <type>Arch2Class</type>
    <class><id>{class_id}</id></class>
    <arch>
        <nodepath>{nodepath}</nodepath>
        <infopath>{infopath}</infopath>
        <valuepath>{valuepath}</valuepath>
    </arch>
</map>"""
    return xml_template

def generarArch2Prop(subject, class_id, predicate, object):
    xml_template = f"""
<map>
    <type>Arch2Prop</type>
    <source>
        <class><id>{class_id}</id></class>
        <arch>
            <nodepath>{subject}</nodepath>
        </arch>
    </source>
    <predicate><id>{predicate}</id></predicate>
    <target>
	    <arch>
		    <valuepath>{object}</valuepath>
	    </arch>
    </target>
</map>"""
    return xml_template

def generarArch2Rel(subject, class_id, predicate, classR_id, subjectR):
    xml_template = f"""
<map>
	<type>Arch2Rel</type>
	<source>
		<class><id>{class_id}</id></class>
		<arch><nodepath>{subject}</nodepath></arch>
	</source>
	<predicate><id>{predicate}</id></predicate>
	<target>
		<class><id>{classR_id}</id></class>
		<arch>
			<nodepath>{subjectR}</nodepath>

		</arch>
	</target>
</map>"""
    return xml_template

def get_keys(d, keys):
    # Get the value of the first key in keys that match a key in d
    for key in keys:
        if key in d:
            return d[key]
    return {}