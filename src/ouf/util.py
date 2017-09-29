
def humanize(bytesize, factor=1024):
    for unit in [_(" bytes"), _("K"), _("M"), _("G"), _("T"), _("P"), _("E"), _("Z"), _("Y")]:
        if bytesize < factor:
            break
        bytesize /= factor
    return "{:.1f}".format(bytesize).rstrip('0').rstrip('.') + unit
