from app.models import *
from app.models.complaint import Complaint, FollowUp
from app import db
from app.models.floodzones import Point, Zone


def init_defaults():

    print(" * Populating the database my friend, just wait...")

    ########################### ZONAS INUNDABLES ############
    zone_cero = Zone(name='Zona Cero', colour="#FF00EE", published=True)

    db.session.add(Point(latitude='-34.903774449680434',
                   longitude='-57.957771179821464', zone=zone_cero))
    db.session.add(Point(latitude='-34.909811761645685',
                   longitude='-57.96354515725', zone=zone_cero))
    db.session.add(Point(latitude='-34.90904232499955',
                   longitude='-57.954162443928624', zone=zone_cero))
    db.session.add(zone_cero)

    zone_uno = Zone(name='Zona Uno', colour="#FF00EE", published=True)

    db.session.add(Point(latitude='-34.9060236963012',
                   longitude='-57.979928818312814', zone=zone_uno))
    db.session.add(Point(latitude='-34.9109363100114',
                   longitude='-57.98584714517706', zone=zone_uno))
    db.session.add(Point(latitude='-34.915315982806696',
                   longitude='-57.97985664359496', zone=zone_uno))
    db.session.add(Point(latitude='-34.90750343015967',
                   longitude='-57.96715389325217', zone=zone_uno))
    db.session.add(zone_uno)

    zone_dos = Zone(name='Zona Dos', colour="#FF00EE", published=True)

    db.session.add(Point(latitude='-34.9263233179962',
                   longitude='-57.93012826285298', zone=zone_dos))
    db.session.add(Point(latitude='-34.93046548102748',
                   longitude='-57.92247774276017', zone=zone_dos))
    db.session.add(Point(latitude='-34.93851251419676',
                   longitude='-57.927602147727995', zone=zone_dos))
    db.session.add(Point(latitude='-34.93750667822358',
                   longitude='-57.93813965653509', zone=zone_dos))
    db.session.add(Point(latitude='-34.93543580061372',
                   longitude='-57.94174839242791', zone=zone_dos))
    db.session.add(zone_dos)

    zona_tres = Zone(name='Aruba', colour="#FF00EE", published=True)

    db.session.add(Point(latitude='-34.911598729026764',
                   longitude='-57.9420016578851', zone=zona_tres))
    db.session.add(Point(latitude='-34.91442360463918',
                   longitude='-57.94516584229556', zone=zona_tres))
    db.session.add(Point(latitude='-34.91509319053249',
                   longitude='-57.94302236253363', zone=zona_tres))
    db.session.add(Point(latitude='-34.913272741123905',
                   longitude='-57.93996024858804', zone=zona_tres))
    db.session.add(zona_tres)

    zona_cuatro = Zone(name='Amazonas', colour="#FF00EE", published=True)

    db.session.add(Point(latitude='-34.92053337356934',
                   longitude='-57.94774312155697', zone=zona_cuatro))
    db.session.add(Point(latitude='-34.92314871776617',
                   longitude='-57.95052454172423', zone=zona_cuatro))
    db.session.add(Point(latitude='-34.92281395836053',
                   longitude='-57.94644172313009', zone=zona_cuatro))

    db.session.add(zona_cuatro)

    ###########################################################
    # creo dos caminos

    camino_negro = Way(
        name='Rivadavia', description="Este camino es el mas facil cuando cae agua", published=True)

    db.session.add(WayPoint(latitude='-34.923900136602924',
                   longitude='-57.94890430361003', route=camino_negro))
    db.session.add(WayPoint(latitude='-34.92210080521731',
                   longitude='-57.94691392954538', route=camino_negro))
    db.session.add(WayPoint(latitude='-34.92364906947575',
                   longitude='-57.94471941455103', route=camino_negro))
    db.session.add(camino_negro)

    camino_gris = Way(
        name='Montevideo', description="Este camino es el camino mas loco", published=True)

    db.session.add(WayPoint(latitude='-34.91954819753631',
                   longitude='-57.95472232015613', route=camino_gris))
    db.session.add(WayPoint(latitude='-34.91657702974311',
                   longitude='-57.95497749631826', route=camino_gris))
    db.session.add(WayPoint(latitude='-34.913940551360604',
                   longitude='-57.95502853155069', route=camino_gris))
    db.session.add(WayPoint(latitude='-34.911429540840885',
                   longitude='-57.952119523302365', route=camino_gris))

    db.session.add(camino_gris)

    #########################################################

    ########################## USUARIOS ########################

    user_admin = User('admin', 'admin', 'admin', 'admin@admin.com', 'asd123')

    op1 = User('erne', 'ernesto', 'guevara', 'erne@gmail.com', '1234')
    op2 = User('erne2', 'ernesto', 'franco', 'franco@gmail.com', '1234')
    op3 = User('herna', 'hernan', 'alonso', 'herna@yahoo.com', '1234')
    op4 = User('horacio', 'horacio', 'fernandez', 'hora@hotmail.com', '1234')
    op5 = User('lamari', 'maria', 'ottalepo', 'lamari@ymail.com', '1234')
    op6 = User('mingo', 'patricio', 'amuchastegui', 'pato@mail.com', '1234')
    op7 = User('conde', 'ramon', 'diaz', 'pelado@gmail.com', '1234')
    op8 = User('pancho', 'francisco', 'solano', 'panchito@gmail.com', '1234')
    op9 = User('ernestin', 'ernesto', 'clausen', 'ern@gmail.com', '1234')
    op9 = User('sergoy', 'sergio', 'goycoechea', 'serg@gmail.com', '1234')
    op10 = User('serpa', 'sergio', 'palavecino', 'pala@gmail.com', '1234')

    operators = (op1, op2, op3, op4, op5, op6, op7, op8, op9, op10)

    ########### MARCO ALGUNOS OPERARIOS COMO BLOQUEADOS #############
    op1.active = False
    op3.active = False
    op5.active = False
    op7.active = False
    op9.active = False

    ########### AGREGO LOS USUARIOS A LA SESION ###############

    db.session.add(user_admin)

    for op in operators:
        db.session.add(op)

    ########################## ROLES #########################

    role_admin = Role(name="Administrador")
    role_op = Role(name="Operador")

    db.session.add(role_admin)
    db.session.add(role_op)

    ########### ASIGNACION DE PERMISOS A ROLES ###############

    role_admin.add_permissions(
        'complaint_create', 'complaint_destroy',
        'complaint_index', 'complaint_show',
        'complaint_update', 'followup_create',
        'followup_destroy', 'followup_index',
        'followup_show', 'followup_update',
        'usuario_destroy', 'punto_encuentro_index', 'punto_encuentro_new', 'punto_encuentro_destroy',
        'punto_encuentro_update', 'punto_encuentro_show', 'usuario_index', 'solicitud_index',
        'usuario_new', 'usuario_change_status', 'usuario_update', 'usuario_show',
        'configuracion_app_update', 'zona_import', 'zona_destroy', 'zona_show', 'zona_index', 'zona_update',
        'evacuacion_index', 'evacuacion_show', 'evacuacion_create', 'evacuacion_destroy', 'evacuacion_update'
    )

    role_op.add_permissions(
        'punto_encuentro_index', 'punto_encuentro_update',
        'punto_encuentro_show', 'usuario_index', 'usuario_show', 'app_privada_update'
        'complaint_create', 'complaint_index', 'complaint_show', 'complaint_update',
        'followup_create', 'followup_index', 'followup_show',
        'followup_update', 'zona_import', 'zona_show', 'zona_index',
        'evacuacion_index', 'evacuacion_show', 'evacuacion_create', 'evacuacion_update'
    )

    ########### ASIGNACION DE ROLES A USUARIOS ###############

    user_admin._roles.append(role_admin)

    for op in operators:
        op._roles.append(role_op)

    ########### PUNTOS DE ENCUENTRO ###############

    punto1 = Location().set_attributes("Estadio Unico",
                                       "unico@unico.com",
                                       "publicado",
                                       "Av. 25, B1900",
                                       "0800-333-unico",
                                       "-34.91375",
                                       "-57.989028")

    punto2 = Location().set_attributes("Catedral de La Plata",
                                       "catedral_lp@info.com",
                                       "despublicado",
                                       "Calle 14, B1900",
                                       "0800-333-catedral",
                                       "-34.922883",
                                       "-57.956317")

    punto3 = Location().set_attributes("Estadio Atenas",
                                       "clubatenas.com",
                                       "despublicado",
                                       "Av. 13 1259, B1904",
                                       "0800-333-atenas",
                                       "-34.925896323817945",
                                       "-57.95178144851603")

    punto4 = Location().set_attributes("SUM Escuela Santa Rosa de Lima",
                                       "santarosa_sum@info.com",
                                       "despublicado",
                                       "Calle punto4",
                                       "0800-333-sum",
                                       "-34.924287443542916",
                                       "-57.90290994769165")

    punto5 = Location().set_attributes("Teatro Argentino",
                                       "teatro_argentino_lp@info.com",
                                       "despublicado",
                                       "Av. 51 702, B1900 AWO",
                                       "0800-333-teatroarg",
                                       "-34.917874",
                                       "-57.9514727")

    punto6 = Location().set_attributes("Teatro Municipal Coliseo Podestá",
                                       "coliseo_podesta@info.com",
                                       "despublicado",
                                       "C. 10 N° 733, B1900",
                                       "0800-333-podesta",
                                       "-34.9157",
                                       "-57.9556")

    punto7 = Location().set_attributes("Pasaje Dardo Rocha",
                                       "pasaje_dardo_rocha@info.com",
                                       "publicado",
                                       "C. 50 575, B1900",
                                       "0800-333-pasaje",
                                       "-34.9140639",
                                       "-57.9498816")

    punto8 = Location().set_attributes("Correo Argentino",
                                       "correo@info.com",
                                       "despublicado",
                                       "Av. 51 456, B1900",
                                       "0800-333-correo",
                                       "-34.9127885",
                                       "-57.9459063")

    punto9 = Location().set_attributes("Hotel Bordo",
                                       "hotelbordo@info.com",
                                       "publicado",
                                       "Av. 137 entre 75 y 76, B1900",
                                       "0800-333-bordo",
                                       "-34.961913",
                                       "-57.9557512")

    punto10 = Location().set_attributes("Supermercado El Nene",
                                        "elnene@info.com",
                                        "publicado",
                                        "Av. 7 2739, B1900",
                                        "0800-333-elnene",
                                        "-34.9372023",
                                        "-57.9198866")

    ########### AGREGO A TODOS LOS PUNTOS DE ENCUENTRO A LA SESION ###############

    db.session.add(punto1)
    db.session.add(punto2)
    db.session.add(punto3)
    db.session.add(punto4)
    db.session.add(punto5)
    db.session.add(punto6)
    db.session.add(punto7)
    db.session.add(punto8)
    db.session.add(punto9)
    db.session.add(punto10)

    ########### CONFIG #################

    Configuration.create_default().save_edit()

    ########## COMPLAINTS ###############

    c1 = Complaint(title='titulo1', desc='desc1', latitude="-34.91375", longitude="-57.989028", surname="Garamond",
                   name="Juan", phone="738347", email="juan@garamond.com", category=1)
    c2 = Complaint(title='titulo2', desc='desc2', latitude="-34.91678", longitude="-57.989123", surname="Gorted",
                   name="Pablo", phone="738347", email="pablo@garamond.com", category=2)
    c3 = Complaint(title='titulo2', desc='desc2', latitude="-34.91678", longitude="-57.989123", surname="Gorted",
                   name="Pablo", phone="738347", email="pablo@garamond.com", category=2)
    c4 = Complaint(title='titulo2', desc='desc2', latitude="-34.91678", longitude="-57.989123", surname="Gorted",
                   name="Pablo", phone="738347", email="pablo@garamond.com", category=2)

    ########### AGREGO A TODAS LAS DENUNCIAS A LA SESION ###############

    db.session.add(c1)
    db.session.add(c2)
    db.session.add(c3)
    db.session.add(c4)

    ######### FOLLOW UPS ################

    f11 = FollowUp(description="desc11", complaint_id=c1.id,
                   author_id=user_admin.id)
    f12 = FollowUp(description="desc12", complaint_id=c1.id, author_id=op1.id)

    f21 = FollowUp(description="desc21", complaint_id=c2.id, author_id=op1.id)
    f22 = FollowUp(description="desc22", complaint_id=c2.id,
                   author_id=user_admin.id)
    f23 = FollowUp(description="desc23", complaint_id=c2.id, author_id=op2.id)

    f31 = FollowUp(description="desc31", complaint_id=c3.id, author_id=op3.id)

    f41 = FollowUp(description="desc41", complaint_id=c4.id, author_id=op4.id)
    f42 = FollowUp(description="desc42", complaint_id=c4.id, author_id=op5.id)

    ########### AGREGO A TODOS LOS PUNTOS DE ENCUENTRO A LA SESION ###############

    db.session.add(f11)
    db.session.add(f12)
    db.session.add(f21)
    db.session.add(f22)
    db.session.add(f23)
    db.session.add(f31)
    db.session.add(f41)
    db.session.add(f42)

    ########### GUARDAR TODO EN LA BD ###############

    db.session.commit()

    ####### el codigo de abajo es de prueba ################################
