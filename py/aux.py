def measure_patch_of_polygons(filename,features): 
    # given the patch filename containing the polygon coordinates, generate morphometrics
    # Polygons are encoded in cartesian coord system (x,y) with the origin at the top-left corner
    # the first 2 integers in the polygon filename give the (x,y) coord of the top-left corner of the patch
    # remember that skimage and numpy use the array convention of (row,col) for coordinates
    data = pd.DataFrame(columns = features) # create empty df to store morphometrics
    df = pd.read_csv(filename)
    nuclei_list = df['Polygon'].tolist()
    #print('There are '+str(len(nuclei_list))+' nuclei in this fov')
    for cell in nuclei_list: # loop over cells in patch
        lista = list(np.fromstring(cell[1:-1], dtype=float, sep=':')) #list of vertices in polygon
        cc = lista[0::2] # list of x coord of each polygon vertex are the columns of a numpy array
        rr = lista[1::2] # list of y coord of each polygon verted are the rows of a numpy array
        poly = np.asarray(list(zip(rr,cc)))
        
        # shift by the min
        mini = np.min(poly,axis=0)
        poly -= mini 
        
        # create the nuclear mask
        mask = np.zeros(tuple(np.ceil(np.max(poly,axis=0) - np.min(poly,axis=0)).astype(int))) # build an empty mask spanning the support of the polygon
        rr, cc = polygon(poly[:, 0], poly[:, 1], mask.shape) # get the nonzero mask locations
        mask[rr, cc] = 1 # nonzero pixel entries
        label_mask = label(mask,connectivity=1) # connectivity has to be 1 otherwise there will be masks from diff nuclei touching on the diagonals
        
        # calculate morphometrics
        dicts = {}
        keys = features         
        try:
            regions = regionprops(label_mask, coordinates='rc')       
            if len(regions) > 0:
                for i in keys:  # loop over features
                    if i == 'centroid_x':
                        dicts[i] = np.rint(regions[0]['centroid'][1]+mini[1]).astype(int) # x-coord is column
                    elif i == 'centroid_y':
                        dicts[i] = np.rint(regions[0]['centroid'][0]+mini[0]).astype(int) # y-coord is row
                    else:
                        dicts[i] = regions[0][i]
        except ValueError:  #raised if array is empty.
            pass
        
        # update morphometrics data 
        new_df = pd.DataFrame(dicts, index=[0])
        data = data.append(new_df, ignore_index=True)
    data.to_pickle(filename+'.morphometrics.pkl')
    return 
