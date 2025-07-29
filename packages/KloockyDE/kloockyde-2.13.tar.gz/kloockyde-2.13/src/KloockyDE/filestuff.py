import win32com.client as wc
from os import listdir, getcwd
from os.path import join, isfile, isdir, splitdrive, splitext, basename, abspath, relpath
from KloockyDE.Algorithms.Sort.quicksort import quicksort_list_asc
from KloockyDE.timestuff import timestamp


def get_file_metadata(path_p, filename_p, metadata_):
    sh = wc.gencache.EnsureDispatch('Shell.Application', 0)
    ns = sh.NameSpace(path_p)

    file_metadata = dict()
    item = ns.ParseName(str(filename_p))
    metadata = ['Name', 'Size', 'Item type', 'Date modified', 'Date created', 'Date accessed', 'Attributes',
                'Offline status', 'Availability', 'Perceived type', 'Owner', 'Kind', 'Date taken',
                'Contributing artists', 'Album', 'Year', 'Genre', 'Conductors', 'Tags', 'Rating', 'Authors',
                'Title',
                'Subject', 'Categories', 'Comments', 'Copyright', '#', 'Length', 'Bit rate', 'Protected',
                'Camera model', 'Dimensions', 'Camera maker', 'Company', 'File description', 'Masters keywords',
                'Masters keywords']
    for ind, attribute in enumerate(metadata):
        attr_value = ns.GetDetailsOf(item, ind)
        if attr_value:
            file_metadata[attribute] = attr_value
    ans = {}
    for x in range(len(metadata_)):
        ans[metadata_[x]] = file_metadata[metadata_[x]]
    return ans


def get_filepaths(dirpath=None, recursive_depth=0, *args, **kwargs):
    '''
    Returns a list of all paths of files in directory 'dirpath'
        paths are dirpath+filename
        recursive: also find files in directories in dirpath
        recursive_depth: How many levels of subdirectories should be checked
            if -1 or True: keep recursion going until no subdirectory contains any directories
            if 0 or False: no recursion
            if > 0 :       up to recursion_depth-many levels of subdirectories will be checked
    :param recursive_depth: int or bool
    :param dirpath: str     path to target directory. Can be relative or absolute. Default: os.getcwd()
    :return:    list of str     list of paths
    '''
    # checks for parameters
    if dirpath is None:     # dirpath default value
        dirpath = getcwd()
    if not isdir(dirpath):  # dirpath not path to a dir?
        raise ValueError('dirpath is not a path to a dir')
    if 'recursive' in list(kwargs.keys()):
        recursive_depth = kwargs['recursive']
    if type(recursive_depth) == bool:   # recursive_depth is bool?
        recursive_depth = int(recursive_depth) * -1     # turn it into int
    elif type(recursive_depth) != int:  # recursive_depth not int?
        raise TypeError('recursive_depth not int')
    elif recursive_depth < -1:          # recursive_depth < -1?
        raise ValueError('recursive_depth < -1')
    # get the paths
    all_paths = [join(dirpath, x) for x in listdir(dirpath)]    # get all paths from files and dirs in directory dirpath
    filepaths = [x for x in all_paths if isfile(x)]     # filter filepaths from all paths
    if recursive_depth != 0:
        if recursive_depth != -1:
            recursive_depth -= 1
        for x in [x for x in all_paths if isdir(x)]:    # filter dirpaths from all paths and do for every path:
            filepaths += get_filepaths(x, recursive_depth)         # recursive step in every dirpath
    return filepaths        # return list of all filepaths


def filename_increment(path_p):
    '''
    Takes file-path 'path_p' and returns next possible filename in its directory
        if path_p does not exist:   return path_p
        else:
            count upwards from 2 and try 'path_p w/o ending'_'number'.'ending' until file does not exist
            return that
    :param path_p: str  : path of file you want to increment
    :return: str : incremented filepath
    '''
    path = path_p[:-len("." + path_p.split(".")[-1])]
    ending = "." + path_p.split(".")[-1]
    f = lambda x: path + "_" + str(x) + ending
    try:
        file = open(path_p, "r", encoding='utf8')
        file.close()
        check = True
        i = 2
        while check:
            try:
                file = open(f(i), "r", encoding='utf8')
                file.close()
                i += 1
            except FileNotFoundError:
                return f(i)
    except FileNotFoundError:
        return path_p


def fi(path):
    '''
    Same as filename_increment but shorter name
    :param path: str  : path of file you want to increment
    :return: str : incremented filepath
    '''
    return filename_increment(path)


def backup(path_dir, path_backup_dir, ausnahmen=[], backup_backups=False, only_txt=True, offset=True, sort=False):
    '''
    backs up files into a file named backup_(timestamp).txt
    :param path_dir:            str:    path of the directory of the files to backup
    :param path_backup_dir:     str:    path where the backup should appear
    :param ausnahmen:           list:   list of names of files, which should not be backed up (strings)
    :param backup_backups:      bool:   False:  backup files will not be backed up
    :param only_txt:            bool:   True:   Only '.txt' files will be backed up
    :param offset:              bool:   True:   an '\t' char will be added to each line of every file
    :param sort:                bool:   True:   List of files gets sorted. Made for sorting ITS/notizen
    :return:                    str:    path to backup file
    '''
    def sorter(l):
        index = {}
        for i in range(len(l)):
            index[int(l[i].split(' ')[1])] = l[i]
        values = quicksort_list_asc(list(index.keys()))
        for i in range(len(values)):
            values[i] = index[values[i]]
        return values
    filenames = [f for f in listdir(path_dir) if isfile(join(path_dir, f))]
    remove = []
    for i in range(len(filenames)):
        if only_txt and not filenames[i][-4:] == '.txt':
            remove.append(i)
        elif not backup_backups and not filenames[i].find('backup') == -1:
            remove.append(i)
        elif filenames[i] in ausnahmen:
            remove.append(i)
    remove.reverse()
    for i in range(len(remove)):
        filenames.pop(remove[i])
    if sort:
        filenames = sorter(filenames)
    backup_name = path_backup_dir + '/backup_' + timestamp() + '.txt'
    backup_file = open(backup_name, 'w', encoding='utf8')
    for i in range(len(filenames)):
        backup_file.write('-----' + filenames[i] + '-----\n')
        file = open(path_dir + '/' + filenames[i], 'r', encoding='utf8')
        for line in file:
            if offset:
                backup_file.write('\t')
            backup_file.write(str(line))
        backup_file.write('\n')
        file.close()
    backup_file.close()
    print('BACKUP SUCCESSFUL RETURNING PATH TO BACKUP FILE')
    return backup_name


def get_lines(path=None):
    '''
    Returns a list of all lines of a file, each as str
        the linebreak at the end of each line is removed
    path has to be path of a file, not dir
    (meant for .txt files, no other filetypes have been tested, use at own risk)
    :param path: str    path to the file
    :return: list of str
    '''
    if path is None:
        raise TypeError('Parameter \'path\' is None (str(path) = \'' + str(path) + '\')')
    if isdir(path):
        raise TypeError('Parameter \'path\' is a path to a directory (has to be to file) (str(path) = \'' + str(path) + '\')')
    if not isfile(path):
        raise TypeError('Parameter \'path\' is not a path (str(path) = \'' + str(path) + '\')')
    lines = []
    file = open(path, 'r', encoding='utf8')
    for x in file:
        line = str(x)
        if line[-1] == '\n':
            lines.append(line[:-1])
        else:
            lines.append(line)
    file.close()
    return lines


def log_line(type_p='INFO', message='DEFAULT LOG LINE'):
    '''
    Returns a line that is good for log-files
        date time type message
    :param type_p:  str :   What type of message? i.e. INFO, ERROR, ...
    :param message: str :   The message
    :return:    str :   line for log-file
    '''
    ans = timestamp().split('_')
    ans[1] = ans[1].replace('-', ':')
    return ans[0] + ' ' + ans[1] + '\t' + type_p + '\t' + message + '\n'


def ispath(path):
    # check type
    try:
        isfile(path)
    except TypeError:
        return False
    # is it real?
    if isrealpath(path):
        return True
    # check type
    if type(path) != str:
        return False
    # check forbidden chars
    bad_chars = '* ? " < > |'.split(' ')
    for c in bad_chars:
        if c in path:
            return False
    # check max one ':'
    if path.count(':') > 1:
        return False
    # check form
    for s in ['//', '\\\\', '/\\', '\\/']:
        if s in path:
            return False
    # check names
    names = []
    for n in path.split('/'):
        names += n.split('\\')
    bad_names = 'CON PRN AUX NUL'.split(' ') + [f'COM{i}' for i in range(1, 10)] + [f'LPT{i}' for i in range(1, 10)]
    bad_names = [n.lower() for n in bad_names]
    for i in range(len(names)):
        n = names[i]
        if n == ('.' * len(n)) and len(n) != 2:
            return False
        if ':' in n:
            if i == 0:
                if n[-1] == ':':
                    return False
            else:
                return False
        if splitext(n)[0].lower() in bad_names:
            return False
        if n[-1] in [' ', '.'] and n != '..':
            return False
    return True


def isrealpath(path):
    try:
        return isfile(path) or isdir(path)
    except TypeError:
        return False


def isabspath(path):
    if not ispath(path):
        return False
    return not splitdrive(path)[0] == ''


def isrelpath(path):
    if not ispath(path):
        return False
    return splitdrive(path)[0] == ''


def ending(filepath):
    '''
    Returns the file-extension of the file at the given path (with the '.')
        Ex: ending('C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe') returns '.exe'
    :param filepath:    str     path to target file
    :return:    str     '.(extension)'
    '''
    # some checks whether filepath is suitable
    if not ispath(filepath):
        raise TypeError('filepath not str')
    if not isfile(filepath):
        raise ValueError('filepath is not a path to a file')
    # the actual "code"
    return '.' + filepath.split('.')[-1]    # split path at '.', take last element in list and re-add the '.'


def get_parentdir_path(path):
    if not ispath(path):
        raise ValueError('path is not a path')
    if isabspath(path):
        return abspath(join(path, '..'))
    else:
        return relpath(join(path, '..'))


def get_parentdir_name(path):
    if not ispath(path):
        raise ValueError('path is not a path')
    path = abspath(path)
    res = basename(abspath(join(path, '..')))
    if res != '':
        return res
    else:
        return splitdrive(path)[0] + '\\'


def get_project_root_path(project_root_dir_name):
    '''
    Returns path to the lowest dir with name project_root_dir_name which is on path to working directory
        lowest means the dir furthest down the path
    :param project_root_dir_name: str   name of dir in path
    :return: absolute path to the dir
    '''
    res = getcwd()
    while basename(res) != project_root_dir_name:
        if basename(res) == '':
            raise ValueError(f'project_root_dir_name "{project_root_dir_name}" not in path')
        res = abspath(join(res, '..'))
    return res
