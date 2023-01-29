def join_group_with_invite_link(self, group_jid, invite_link):
    """
    Join into a specific group, using an invite link.
    :param group_jid: The JID of the same group
    :param invite_link: An invite code (Looks like kik.me/g/{random characters})
    """
    log.info("[+] Joining the group '{}' with JID {}".format(invite_link, group_jid))
    return self._send_xmpp_element(roster.JoinByInviteLinkRequest(group_jid, invite_link))
