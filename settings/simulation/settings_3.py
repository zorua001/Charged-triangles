from config.allowed_bodies import Body

SIMULATION_PARAMS = {
    #Which charge distribution is used. Options are point_charge, homogenous
    'charge_distribution_method': 'point_charge',
    #Which method for finding field points is used. Options are centroid, triple
    'field_point_method': 'triple',
    #If you have field_point_method 'triple' you need an offset variable which is a float between 0 and 1
    'offset':float(0.5),
    #Which geometric bodies exist in this setup (see file allowed_bodies)
    'bodies': ([
        Body('cylinder', float(5), pos=[.5,.5,-1.5],rot=[0,0,0], radius=0.5, height=5,length_resolution=20, height_resolution=20),
        Body('box', pos = [0,0,0],rot =[0,0,0], height=3 , width = 3, depth = 3, iterations = 4 )
        ])
}