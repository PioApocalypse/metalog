import os
import json, re
from datetime import datetime
from dateutil.tz import tzlocal
import elabapy

class Manager():

    def __init__(self, endpoint, token):
        """Class representing an elabFTW Manager

        Args:
            endpoint: endpoint to initialize the elabFTW Manager (e.g. "https://elab.example.org/api/v1")
            token: token to access the elabFTW Manager (e.g. "55cde...403157")

        Return: None
        """

        # Initialize elabFTW Manager
        self.endpoint = endpoint
        self.instance = elabapy.Manager(endpoint=endpoint, token=token)

    def __repr__(self):
        return "elabFTW Manager at {}.".format(self.endpoint)
    
    def get_experiments(self,
                        expid=None,
                        title=None,
                        date=None,
                        category=None,
                        userid=None,
                        tags=None
                        ):
        """ Get a list of experiments which match all the given properties

        Args:
            expid: (integer, optional) id of the experiment
            title: (string, optional) title of the experiment
            date: (string, optional) date of the experiment
            category: (string, optional) category of the experiment
            userid: (integer, optional) userid of the experiment
            tags: (list, optional) list of tags of the experiment

        Return:
            List of experiments
        """

        all_exp = self.instance.get_all_experiments()

        if expid != None:
            all_exp = [exp for exp in all_exp if int(exp['id']) == expid]
        if title != None:
            all_exp = [exp for exp in all_exp if exp['title'] == title]
        if date != None:
            all_exp = [exp for exp in all_exp if exp['date'] == date]
        if category != None:
            all_exp = [exp for exp in all_exp if exp['category'] == category]
        if userid != None:
            all_exp = [exp for exp in all_exp if int(exp['userid']) == userid]
        if tags != None:
            for tag in tags:
                all_exp = [exp for exp in all_exp if tag in exp['tags']]

        return all_exp

    def get_experiment(self,
                       expid):
        """ Get experiment with given id

        Args:
            expid: (integer) id of the experiment

        Return:
            Experiment instance
        """

        exp = self.get_experiments(expid=expid)[0]

        return Experiment(self.instance, expid=int(exp['id']))

    def create_experiment(self,
                          title=None,
                          date=None,
                          category=None,
                          userid=None,
                          tags=None,
                          links=None,
                          metadata=None,
                          body=None):
        """ Create a new experiment with the given properties

        Args:
            title: (string, optional) title of the experiment
            date: (string, optional) date of the experiment
            category: (string, optional) category of the experiment
            userid: (integer, optional) userid of the experiment
            tags: (list, optional) list of tags of the experiment
            links: (list, optional) list of integers representing links to items
            metadata: (dictionary, optional) dictionaty of metadata to be attached to the experiment
            body: (string, optional) body text

        Return:
            Experiment instance
        """

        return Experiment(self.instance,
                          title=title,
                          date=date,
                          category=category,
                          userid=userid,
                          tags=tags,
                          links=links,
                          metadata=metadata,
                          body=body)

    def get_all_items(self, **kwargs):
        """ Get all items from database

        Return:
            List of items
        """

        return self.instance.get_all_items(**kwargs)

    def get_item(self,
                 item_id):
        """ Get item with given id

        Args:
            item_id: (integer) id of the item

        Return:
            Item
        """

        return self.instance.get_item(item_id)

    def get_all_status(self):
        """ Get list of available experiment statuses/categories

        Return:
            List of dictionaries of statuses/categories
        """

        return self.instance.get_status()

    def get_items_types(self):
        """ Get list of existing items types/categories

        Return:
            List of dictionaries of items types/categories
        """

        return self.instance.get_items_types()

class Experiment():

    def __init__(self,
                 instance,
                 expid=None,
                 title=None,
                 date=None,
                 category=None,
                 userid=None,
                 tags=None,
                 links=None,
                 metadata=None,
                 body=None):
        """Class representing an elabFTW Experiment

        Args:
            instance: instance of elab.Manager() in wich create the Experiment
            expid: (integer, optional) ID of an existing Experiment to be accessed. If not given a new Experiment is created.
            title: (string, optional) title of the experiment
            date: (string, optional) date of the experiment
            category: (string, optional) category of the experiment
            userid: (integer, optional) userid of the experiment
            tags: (list, optional) list of tags of the experiment
            links: (list, optional) list of integers representing links to items
            metadata: (dictionary, optional) dictionaty of metadata to be attached to the experiment
            body: (string, optional) body text

        Return: None
        """

        # Set elabFTW Manager
        self.manager = instance

        # Get Experiment ID
        if expid:
            self.expid = expid
        else:
            response = self.manager.create_experiment()
            self.expid = int(response['id'])

        # Get elabFTW Experiment instance
        self.exp = self.manager.get_experiment(self.expid)

        # Set properties
        self.update(title,
                    date,
                    category,
                    userid,
                    tags,
                    links,
                    metadata,
                    body)

    def update(self,
               title=None,
               date=None,
               category=None,
               userid=None,
               tags=None,
               links=None,
               metadata=None,
               body=None):
        """ Update experiment properties

        """

        if title != None:
            params = { "title": title }
            print(self.manager.post_experiment(self.expid, params))
        if date != None:
            params = { "date": date }
            print(self.manager.post_experiment(self.expid, params))
        if category != None:
            params = { "category": category }
            print(self.manager.post_experiment(self.expid, params))
        if userid != None:
            params = { "userid": userid }
            print(self.manager.post_experiment(self.expid, params))
        if tags != None:
            for tag in tags:
                params = { "tag": tag }
                print(self.manager.post_experiment(self.expid, params))
        if metadata != None:
            params = { "metadata": json.dumps(metadata) }
            print(self.manager.post_experiment(self.expid, params))
        if body != None:
            params = { "body": body }
            print(self.manager.post_experiment(self.expid, params))
        if links != None:
            for link in links:
                params = { "link": link }
                print(self.manager.add_link_to_experiment(self.expid, params))

    def __repr__(self):
        self.get()
        return json.dumps(self.exp, indent=4, sort_keys=True)

    def get(self):
        """ Get updated experiment instance

        """
        self.exp = self.manager.get_experiment(self.expid)

    def get_body(self):
        """ Simply return the Experiment body as a string

        """
        self.get()
        return self.exp["body"]

    def replace_body(self, new_body):
        """ Replace Experiment body
        
        Args:
            new_body: string of the new Experiment body
        
        Return: nothing
        """

        params = { "body": new_body }
        print(self.manager.post_experiment(self.expid, params))

    def append_to_body(self, text):
        """ Append text to the Experiment body
        
        Args:
            text: string of text to be appended to the Experiment body
        
        Return: nothing
        """

        params = { "bodyappend": text }
        print(self.manager.post_experiment(self.expid, params))

    def add_meta(self, meta_dict):
        """ Add JSON metadata to the Experiment
        
        Args:
            meta_dict: dictionary of metadata to be added to the Experiment as JSON
        
        Return: nothing
        """

        params = { "metadata": str(meta_dict) }
        print(self.manager.post_experiment(self.expid, params))

    def get_meta(self):
        """ Get JSON metadata to the Experiment
        
        Return: dictionary of metadata of the Experiment
        """

        self.get()
        return json.loads(self.exp["metadata"])

    def append_meta(self, meta_dict):
        """ Append JSON metadata to the Experiment
        
        Args:
            meta_dict: dictionary of metadata to be appended to the Experiment as JSON
        
        Return: nothing
        """

        meta_dict.update(self.get_meta())

        params = { "metadata": json.dumps(meta_dict) }
        print(self.manager.post_experiment(self.expid, params))

    def upload_file(self, file_path):
        """Upload binary file to an Experiment

        Args:
            file_path: full path to the file

        Return: None
        """

        try:
            with open(file_path, 'rb') as f:
                params = { 'file': f }
                print("Upload", file_path, self.manager.upload_to_experiment(self.expid, params))
            self.get()
            return True
        except FileNotFoundError:
            print("{} file not found! Skipped.".format(file_path))
            return False

    def insert_image(self, image_path, res=None, wh="width", append=True, html=False):
        """Upload image to an Experiment and insert it in the body

        Args:
            image_path: full path to the image to upload
            res: (optional) pixel resolution of the image along dimension specified by wh
            wh: (optional) equal to "width" (default) or "height"
            append: boolean indicating if inserting the image in the body (default True)
            html: whether return image link in html (default False)

        Return: markdown code of the image link
        """

        # Upload image to Experiment
        status = self.upload_file(image_path)

        # Get long_name of the image
        if status:
            image_name = os.path.basename(image_path)
            for item in self.exp['uploads']:
                if item['real_name'] == image_name:
                    long_name = item['long_name']
                    # Generate HTML code
                    if res:
                        html_code = '<img src="app/download.php?f={}" {}="{}" />'.format(long_name, wh, res)
                    else:
                        html_code = '<img src="app/download.php?f={}" />'.format(long_name)

                    if html:
                        html_code = '<p>'+html_code+'</p>\n'
                    else:
                        html_code = html_code+'\n'

                    # Append to body
                    if append:
                        self.append_to_body(html_code)

                    return html_code
                else:
                    return ""
        else:
            return ""

    def _get_cells_meta(self):
        """ Get metadata of the cells within the Experiment body

        A dictionary is returned in which keys are cells IDs and
        values are dictionaries of the metadata ("tags", "datetime").

        Return: dictionary of cell metadata.
        """

        # Get Experiment body
        body = self.get_body()
        
        # Split body into cells
        start = ' data-cell-id='
        reList = re.split(start, body)
        
        # Initialize and populate dictionary of the cells
        cells = dict()
        for r in reList:
            m = re.match(r'\"(\d+)\" data-cell-tags=\"(.+)\" data-cell-datetime=\"(.+)\">', r)
            groups = m.groups()
            d = dict()
            d["tags"] = json.loads(groups[1])
            d["datetime"] = groups[2]
            cells[int(groups[0])] = d

        return cells

    def _get_max_cell_id(self):
        """ Return the maximum ID of the cells in the Experiment body

        """

        cells = self.get_cells_meta()
        if len(cells) != 0:
            return max(cells.keys())
        else:
            return -1

    def _add_cell(self, text, tags=list(), title=""):
        """ Add a new cell with the given content to the Experiment body

        Args:
            text: HTML code content of the cell.
            tags: (optional) list of the tags associated to the cell.
            title: (optional) string showed when hovering the mouse on the cell.

        Return: nothing.
        """

        # Get new cell ID
        cell_id = self._get_max_cell_id() + 1

        # Generate HTML code for the cell
        timestamp = datetime.now(tzlocal()).replace(microsecond=0).isoformat()
        HTML_code = '<div title="{}" data-cell-id="{}" data-cell-tags="{}" data-cell-datetime="{}">\n'.format(cell_id, tags, timestamp, title)
        HTML_code += text
        HTML_code += '\n</div>\n'

        # Append cell code to Experiment body
        self.append_to_body(HTML_code)

    def _get_cell(self, cell_id):
        pass

    def _replace_cell(self, cell_id, text):
        pass
