class SortableHeader(object):
    def __init__(self, name, sortable, verbose_name = '', class_name = '', attribs = ''):
        self.name = name
        self.sortable = sortable
        self.verbose_name = verbose_name
        self.ordering = ''
        self.removable = ''
        self.class_name = class_name
        self.sort_type = ''
        self.order = 0
        self.attribs = attribs
        
def get_field_index(raw_get_data):#returns array of header ids
    if raw_get_data and  raw_get_data!='[]':
        field_index = list(map(int,raw_get_data.split('.')))
        return field_index
    return None
        

def get_sorted_list(request, obj, fields_list, raw_get_data):
    field_index = get_field_index(raw_get_data)
    if field_index:
        sort_order = [fields_list[abs(x)].name if x >0 else f'-{fields_list[abs(x)].name}' for x in field_index ]
        if sort_order:
            obj = obj.order_by(*sort_order)
            return obj
    return obj
        
def get_ordering(ordering, unsigned_index, signed_index, sign_to_add):#[1,2],1,-1,-
    rem = None
    removable = ''
    print(f"unsigned_index, signed_index ------ {unsigned_index}, {signed_index}")
    if ordering:
        if signed_index in ordering:
            rem = ordering.copy()
            ord = ordering.copy()
            ord.insert(0,str(-1*int(signed_index)))
            ord.remove(signed_index)
            rem.remove(signed_index)
        else:
            rem = None
            ord = ordering.copy()
            ord.insert(0,unsigned_index)
        if ord:      
            ord = '.'.join(list(map(str,ord)))
        if rem:
            rem = '.'.join(list(map(str,rem)))
        return ord,rem
    else:
        return unsigned_index,None
                       
def get_sortable_header(header, ordering, getValue):
    context = {}
    l = len(header) + 1
    headers = []
    descending_list = []
    ascending_list = []
    if ordering:
        counter = 1
        for order in ordering:
            header[abs(order)].order = counter
            if order < 0:
                descending_list.append(header[abs(order)].name)
            else:
                ascending_list.append(header[abs(order)].name)
            counter = counter + 1
    
    for row in range(1,l):
       class_name = 'col-' + header[row].name
       if ordering:
        signed_index = -1*row if -1*row in ordering else row
       else:
        signed_index = row
       if header[row].sortable:
           class_name = class_name + ' sortable'
           sign_str = ''
           if header[row].name in ascending_list:
               class_name = 'sorted ascending ' + class_name
               header[row].sort_type = 'ascending'
           elif header[row].name in descending_list:
               class_name = 'sorted descending ' + class_name
               header[row].sort_type = 'descending'
               signed_index = signed_index * -1
           header[row].ordering, header[row].removable = get_ordering(ordering, row, signed_index, sign_str)
           header[row].class_name = header[row].class_name + ' ' + class_name
       headers.append(header[row]) 
    context['headers'] = headers
    context['getValue'] = getValue
    return context