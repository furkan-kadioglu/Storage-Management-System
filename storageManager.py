

# In[1]:


import os
import shutil as sh
import pickle as pk
import sys


# In[3]:


f = open(sys.argv[1], 'r')
s = f.readlines()
out_file = sys.argv[2]
open(out_file, 'w').close()

# In[4]:


def filterspace(x):
    while True:
        try:
            x.remove('')
        except:
            return x


queries = [filterspace(i.strip().split(' ')) for i in s]


# ## DDL Operations

# In[5]:


def create_type(query):
    try:
        with open('system_catolog.pickle', 'rb') as f:
            sys_catalog = pk.load(f)
            f.close()
    except:
        sys_catalog = []

    if not (True in [i[0] == query[2] for i in sys_catalog]):
        sys_catalog.append([query[2], int(query[3])])
        os.makedirs('files/'+query[2])
        with open('files/'+query[2]+'/0.pickle', 'wb') as f:
            pk.dump([], f, pk.HIGHEST_PROTOCOL)
            f.close()

    with open('system_catolog.pickle', 'wb') as f:
        pk.dump(sys_catalog, f, pk.HIGHEST_PROTOCOL)
        f.close()


def list_type(query):
    try:
        with open('system_catolog.pickle', 'rb') as f:
            sys_catalog = pk.load(f)
            f.close()
    except:
        sys_catalog = []

    names = sorted([i[0] for i in sys_catalog])

    for i in names:
        with open(out_file, 'a')as f:
            f.write(str(i)+'\n')
            f.close()


def delete_type(query):
    try:
        with open('system_catolog.pickle', 'rb') as f:
            sys_catalog = pk.load(f)
            f.close()
    except:
        sys_catalog = []

    if True in [i[0] == query[2] for i in sys_catalog]:
        transpose_catalog = list(map(list, zip(*sys_catalog)))
        sys_catalog.pop(transpose_catalog[0].index(query[2]))
        with open('system_catolog.pickle', 'wb') as f:
            pk.dump(sys_catalog, f, pk.HIGHEST_PROTOCOL)
            f.close()
        sh.rmtree('files/'+query[2])


# ## DML Operations

# In[6]:


def create_rec(query):
    try:
        with open('system_catolog.pickle', 'rb') as f:
            sys_catalog = pk.load(f)
            f.close()
    except:
        sys_catalog = []

    if True in [i[0] == query[2] for i in sys_catalog]:

        transpose_catalog = list(map(list, zip(*sys_catalog)))
        rec_type = sys_catalog.pop(transpose_catalog[0].index(query[2]))

        if (len(query) - 3) == rec_type[1]:
            insert(query)

# searches available position for new record.


def insert(query):
    page_no = 0
    while True:
        try:
            with open('files/'+query[2]+'/'+str(page_no)+'.pickle', 'rb') as f:
                page = pk.load(f)
                f.close()
            if len(page) < (400 / (len(query)-3)):
                page.append([int(i) for i in query[3:]])
                break
            else:
                page_no += 1
        except:
            page = [[int(i) for i in query[3:]]]
            break

    with open('files/'+query[2]+'/'+str(page_no)+'.pickle', 'wb') as f:
        pk.dump(page, f, pk.HIGHEST_PROTOCOL)
        f.close()


# In[7]:


def delete_rec(query):
    try:
        with open('system_catolog.pickle', 'rb') as f:
            sys_catalog = pk.load(f)
            f.close()
    except:
        sys_catalog = []

    if True in [i[0] == query[2] for i in sys_catalog]:
        delete(query)


def delete(query):
    page_no = 0
    while True:
        try:
            with open('files/'+query[2]+'/'+str(page_no)+'.pickle', 'rb') as f:
                page = pk.load(f)
                f.close()
            try:
                transpose_page = list(map(list, zip(*page)))
                page.pop(transpose_page[0].index(int(query[3])))

                with open('files/'+query[2]+'/'+str(page_no)+'.pickle', 'wb') as f:
                    pk.dump(page, f, pk.HIGHEST_PROTOCOL)
                    f.close()
                break
            except:
                page_no += 1
        except:
            break


# In[8]:


def update_rec(query):
    try:
        with open('system_catolog.pickle', 'rb') as f:
            sys_catalog = pk.load(f)
            f.close()
    except:
        sys_catalog = []

    if True in [i[0] == query[2] for i in sys_catalog]:
        transpose_catalog = list(map(list, zip(*sys_catalog)))
        rec_type = sys_catalog.pop(transpose_catalog[0].index(query[2]))

        if (len(query) - 3) == rec_type[1]:
            update(query)


def update(query):
    page_no = 0
    while True:
        try:
            with open('files/'+query[2]+'/'+str(page_no)+'.pickle', 'rb') as f:
                page = pk.load(f)
                f.close()
            try:
                transpose_page = list(map(list, zip(*page)))
                page.pop(transpose_page[0].index(int(query[3])))
                page.append([int(i) for i in query[3:]])
                with open('files/'+query[2]+'/'+str(page_no)+'.pickle', 'wb') as f:
                    pk.dump(page, f, pk.HIGHEST_PROTOCOL)
                    f.close()
                break
            except:
                page_no += 1
        except:
            break


# In[9]:


def search_rec(query):
    try:
        with open('system_catolog.pickle', 'rb') as f:
            sys_catalog = pk.load(f)
            f.close()
    except:
        sys_catalog = []

    if True in [i[0] == query[2] for i in sys_catalog]:
        page_no = 0
        while True:
            try:
                with open('files/'+query[2]+'/'+str(page_no)+'.pickle', 'rb') as f:
                    page = pk.load(f)
                    f.close()
                try:
                    transpose_page = list(map(list, zip(*page)))
                    record = page.pop(transpose_page[0].index(int(query[3])))

                    record = ' '.join([str(a) for a in record])
                    with open(out_file, 'a')as f:
                        f.write(record+'\n')
                        f.close()
                    break
                except:
                    page_no += 1
            except:
                break


# In[10]:


def list_rec(query):
    all_records = []
    try:
        with open('system_catolog.pickle', 'rb') as f:
            sys_catalog = pk.load(f)
            f.close()
    except:
        sys_catalog = []

    if True in [i[0] == query[2] for i in sys_catalog]:
        page_no = 0
        while True:
            try:
                with open('files/'+query[2]+'/'+str(page_no)+'.pickle', 'rb') as f:
                    page = pk.load(f)
                    f.close()

                all_records += page
                page_no += 1
            except:
                break
        for record in sorted(all_records):
            record = ' '.join([str(a) for a in record])
            with open(out_file, 'a')as f:
                f.write(record+'\n')
                f.close()


# In[11]:


# Query Redirection
for i in queries:

    if len(i) < 2:
        continue
    # DDL Operations
    if i[1] == 'type':
        if i[0] == 'create':
            create_type(i)
            continue
        if i[0] == 'delete':
            delete_type(i)
            continue
        if i[0] == 'list':
            list_type(i)
            continue

    # DML Operations
    elif i[1] == 'record':
        if i[0] == 'create':
            create_rec(i)
            continue
        if i[0] == 'delete':
            delete_rec(i)
            continue
        if i[0] == 'list':
            list_rec(i)
            continue
        if i[0] == 'update':
            update_rec(i)
            continue
        if i[0] == 'search':
            search_rec(i)
            continue
