import os
import argparse
import configparser
from collections import OrderedDict
import shutil

config = configparser.ConfigParser()
config.read('config.ini')

DATA_PATH = os.path.join(config['path']['path'].replace('/', '\\'), 'Data')
SCRIPTS_PATH = os.path.join(
    config['path']['path'].replace('/', '\\'), 'Scripts')


class CreateHandler:
    '''
    Handler class for `create` command.
    '''

    def __init__(self, args):
        self._args = args

    def parse(self):
        if len(self._args.project) == 0:
            print('You dont enter any project to create!')
            return
        else:
            self.create_project(self._args.project)

    @staticmethod
    def create_project(projectnames: list):
        # use set to exclude repeated projects
        for pname in OrderedDict.fromkeys(projectnames):
            # fix bugs
            pname.replace(' ', '_')

            data_pname_path = os.path.join(DATA_PATH, pname)
            scripts_pname_path = os.path.join(SCRIPTS_PATH, pname)
            # Create project in Data folder
            if os.path.exists(data_pname_path):
                print(f'Err: Project {pname} always exist in \"{DATA_PATH}\"!')
            else:
                # create project
                os.mkdir(data_pname_path)
                print(f'Create {pname} in {DATA_PATH}')
            # Create project in Scripts folder
            if os.path.exists(scripts_pname_path):
                print(
                    f'Err: Project {pname} always exist in \"{SCRIPTS_PATH}\"!')
            else:
                # create project
                os.mkdir(scripts_pname_path)
                print(f'Create {pname} in {SCRIPTS_PATH}')


class DeleteHandler:
    '''
    Handler class for `delete` command.
    '''

    def __init__(self, args):
        self._args = args

    def parse(self):
        if not self._args.all and len(self._args.project) == 0:
            print('You dont enter any project to delete!')
            return
        else:
            self.delete_projects(self._args.project, self._args.all)

    @staticmethod
    def delete_projects(projectnames: list, all=False):

        if all:
            data_arr = os.listdir(DATA_PATH)
            scripts_arr = os.listdir(SCRIPTS_PATH)

            for pname in data_arr:
                shutil.rmtree(os.path.join(DATA_PATH, pname))
            for pname in scripts_arr:
                shutil.rmtree(os.path.join(SCRIPTS_PATH, pname))
            print('Delete all projects.')

            return

        # use OrderedDict to exclude repeated projects
        for pname in OrderedDict.fromkeys(projectnames):
            # fix bugs
            pname.replace(' ', '_')

            data_pname_path = os.path.join(DATA_PATH, pname)
            scripts_pname_path = os.path.join(SCRIPTS_PATH, pname)

            if os.path.exists(data_pname_path):
                # remove project
                shutil.rmtree(data_pname_path)
                print(f'Delete {pname} in \"{DATA_PATH}\"')
            else:
                print(
                    f'Err: Project {pname} always deleted in \"{DATA_PATH}\"!')

            if os.path.exists(scripts_pname_path):
                # remove project
                shutil.rmtree(scripts_pname_path)
                print(f'Delete {pname} in \"{SCRIPTS_PATH}\"')
            else:
                print(
                    f'Err: Project {pname} always deleted in \"{SCRIPTS_PATH}\"!')


class ListHandler:
    '''
    Handler class for `list` command.
    '''

    def __init__(self, args):
        self._args = args

    def parse(self):
        self.get_list_of_projects()

    @staticmethod
    def get_list_of_projects():

        data_arr = os.listdir(DATA_PATH)
        scripts_arr = os.listdir(SCRIPTS_PATH)

        union_set = set(data_arr).union(scripts_arr)
        print('Projects:')
        for project in union_set:
            if project in data_arr and project in scripts_arr:
                print(f'- {project}')
            elif project in data_arr:
                print(f'- {project} | just in /Data/')
            elif project in scripts_arr:
                print(f'- {project} | just in /Scripts/')


class CustomHelpFormatter(argparse.HelpFormatter):
    def _format_action(self, action):
        if type(action) == argparse._SubParsersAction:
            # inject new class variable for subcommand formatting
            subactions = action._get_subactions()
            invocations = [self._format_action_invocation(
                a) for a in subactions]
            self._subcommand_max_length = max(len(i) for i in invocations)

        if type(action) == argparse._SubParsersAction._ChoicesPseudoAction:
            # format subcommand help line
            subcommand = self._format_action_invocation(action)  # type: str
            width = self._subcommand_max_length
            help_text = ""
            if action.help:
                help_text = self._expand_help(action)
            return "  {:{width}} -  {}\n".format(subcommand, help_text, width=width)

        elif type(action) == argparse._SubParsersAction:
            # process subcommand help section
            msg = '\n'
            for subaction in action._get_subactions():
                msg += self._format_action(subaction)
            return msg
        else:
            return super(CustomHelpFormatter, self)._format_action(action)


class CommonHandler:

    commands_dict = {
        'create': CreateHandler,
        'delete': DeleteHandler,
        'list': ListHandler
    }

    @staticmethod
    def init():
        parser = argparse.ArgumentParser(
            usage='python manage_projects.py <command>', formatter_class=CustomHelpFormatter)

        subparsers = parser.add_subparsers(
            title='commands', help='command help', dest='subparser_name')
        # --- create
        parser_create = subparsers.add_parser(
            'create', help='create project or projects')
        parser_create.add_argument('project', type=str, nargs='*')
        # --- delete
        parser_delete = subparsers.add_parser(
            'delete', help='delete project or projects')
        parser_delete.add_argument('project', type=str, nargs='*')
        parser_delete.add_argument('--all', action='store_true')
        # --- list
        parser_list = subparsers.add_parser(
            'list', help='view info about created projects')
        parser_list.add_argument('--meta', action='store_true',
                                 help='view add info about projects in Task Sheduler')

        args = parser.parse_args()

        # subparser_name: dest='subparser_name' arguments in add_subparsers method
        if args.subparser_name is None:
            parser.print_help()
            return

        # process the command entered
        ClassHandler = CommonHandler.commands_dict[args.subparser_name]
        obj = ClassHandler(args)
        obj.parse()


def main():
    CommonHandler.init()


if __name__ == '__main__':
    main()
