import posixpath


def isabs(path):
    return path.startswith('/')


def split(path):
    if '/' not in path:
        return '', path

    path_data = path.rsplit('/', 1)

    if isabs(path) and len(path_data[0]) == 0:
        return '/', path_data[1]

    return path_data


def normpath(path):
    return posixpath.normpath(path)


def join(a, *p):
    """Join two or more pathname components, inserting '/' as needed.
    If any component is an absolute path, all previous path components
    will be discarded.  An empty last part will result in a path that
    ends with a separator."""

    sep = '/'
    path = a

    try:
        for b in p:
            if b.startswith(sep):
                path = b
            elif not path or path.endswith(sep):
                path += b
            else:
                path += sep + b
    except TypeError:
        valid_types = all(isinstance(s, (str, bytes, bytearray))
                          for s in (a,) + p)
        if valid_types:
            # Must have a mixture of text and binary data
            raise TypeError("Can't mix strings and bytes in path "
                            "components.") from None
        raise
    return path


def shortfilename(filename, initials_counts):
    invalid_chars = """"/\\[]:;=,"""

    if len(filename) > 8 or ' ' in filename:
        filename = filename.upper()

        new_filename = ''
        extension = ''
        past_extension = ''

        corrupted = False

        last_dot_index = None
        second_last_dot_index = None

        for index, char in enumerate(filename):
            if char not in invalid_chars and char != ' ':
                if char == '.':
                    past_extension = extension
                    extension = ''
                    second_last_dot_index = last_dot_index
                    last_dot_index = index
                    corrupted = False
                    continue

                if last_dot_index is not None:
                    if len(extension) < 3:
                        extension += char
                else:
                    if len(new_filename) < 6:
                        new_filename += char
            else:
                if last_dot_index is not None:
                    corrupted = True
                    continue

        initials = new_filename

        try:
            count = initials_counts[initials]
        except KeyError:
            initials_counts[initials] = 0
            count = 1

        initials_counts[new_filename] += 1

        return new_filename + '~%i' % count + ('.' if (extension or past_extension) else '') + (past_extension if corrupted or len(extension) == 0 else extension)

    else:
        return ''
