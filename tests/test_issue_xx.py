"""a template for creating tests that display or duplicate issues"""

from __future__ import print_function

# pylint: disable = W0142
from common import VFS, conn, pysftp


# this is the preferred test type as it can be run on the CI server and
# requires no configuarion of a real sftp server.  However issues that involve
# authentication and/or authorization currently have to use a real sftp
# server (see test_issue_xx_lsftp)
def test_issue_xx_sftpserver_plugin(sftpserver):
    '''an example showing how to use the sftpserver plugin in a test'''
    with sftpserver.serve_content(VFS):
        with pysftp.Connection(**conn(sftpserver)) as sftp:
            home = sftp.pwd
            with sftp.cd():
                sftp.chdir('pub')
                assert sftp.pwd == '/home/test/pub'
            assert home == sftp.pwd


def test_issue_xx_local_sftpserver(lsftp):
    '''same as test_issue_xx_sftpserver_plugin but written with the local
    sfptserver mechanism, lsftp'''
    home = lsftp.pwd
    # starting condition of default directory should be empty, so we need to
    # construct whatever structure we need prior to peforming the test
    lsftp.mkdir('pub')
    # now the test phase
    with lsftp.cd():
        lsftp.chdir('pub')
        # don't throw an assert until after cleanup, just save result for later
        pubdir = lsftp.pwd == '/home/test/pub'
    homedir = home == lsftp.pwd
    # cleanup the remote directory back to pristine (empty)
    lsftp.rmdir('pub')  # clean up remote dir back to pristine
    # now we make our assertions
    assert pubdir       # test the assertions AFTER we cleanup
    assert homedir

