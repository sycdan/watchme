'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from watchme.utils import generate_temporary_file
from watchme.logger import bot
from requests.exceptions import HTTPError
import tempfile
import requests


def get_task(url, **kwargs):
    '''a simple task to use requests to get a url. By default, we return
       the raw response.

       Parameters
       ==========

       REQUIRED:
           url: a url to return the page for
    '''
    result = None
    response = requests.get(url)
    if response.status_code == 200:
        save_as = kwargs.get('save_as')

        # Returning the result as json will detect dictionary, and save json
        if save_as == "json":
            result = response.json()

        # Otherwise, we return text
        else:
            result = response.text
    return result


def post_task(url, **kwargs):
    '''a simple task to use requests to post to. By default, we return json.

       Parameters
       ==========

       REQUIRED:
           url: a url to post to
    '''
    result = None
    response = requests.post(url)
    if response.status_code == 200:

        save_as = kwargs.get('save_as', 'json')

        # Returning the result as json will detect dictionary, and save json
        if save_as == "json":
            result = response.json()

        # Otherwise, we return text
        else:
            result = response.text
    return result


def download_task(url, **kwargs):
    '''a simple task to use requests to get a url. By default, we return
       the raw response.

       Parameters
       ==========

       REQUIRED:
           url: a url to download (stream)

       OPTIONAL:
           write_format: to change from default "w"
           disable_ssl_check: set to anything to not verify (not recommended)
    '''
    result = None

    # Update the user what we are doing
    bot.verbose("Downloading %s" % url)

    # Use the basename or the user set file_name to write to
    file_name = kwargs.get('file_name', os.path.basename(url))

    # Generate a temporary object for the file
 or generate_temporary_file()
    
    destination = generate_temporary_file()
    verify = True

    # Does the user want to disable ssl?
    if "disable_ssl_check" in kwargs:
        if kwargs['disable_ssl_check']:
            bot.warning('Verify of certificates disabled! ::TESTING USE ONLY::')
            verify = False

    # If the user doesn't want to write, but maybe write binary
    fmt = kwargs.get('write_format', 'w')

    # Does the url being requested exist?
    if requests.head(url, verify=verify).status_code in [200, 401]:

        # Stream the response
        response = requests.get(url, verify=verify, stream=True)

        # Invalid permissions
        if response.status_code == 401:
            return result

        # Successful, stream to result destination
        if response.status_code == 200:

            chunk_size = 1 << 20
            with open(destination, fmt) as filey:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    filey.write(chunk)

            result = destination

    return result
