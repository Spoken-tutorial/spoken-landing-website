from django import template
import zipfile
import os
from django.conf import settings

register = template.Library()
def get_zip_content(path):
    file_names = None
    try:
        zf = zipfile.ZipFile(path, 'r')
        file_names = zf.namelist()
        return file_names
    except Exception as e:
        return False

def get_review_status_list(key):
	status_list = ['Pending', 'Waiting for Admin Review', 'Waiting for Domain Review', 'Waiting for Quality Review', 'Accepted', 'Need Improvement', 'Not Required']
	return status_list[key]

def get_review_status_symbol(key):
	status_list = ['fa fa-1 fa-minus-circle review-pending-upload', 'fa fa-1 fa-check-circle review-admin-review', 'fa fa-1 fa-check-circle review-domain-review', 'fa fa-1 fa-check-circle review-quality-review', 'fa fa-1 fa-check-circle review-accepted', 'fa fa-1 fa-times-circle review-pending-upload', 'fa fa-1 fa-ban review-accepted']
	return status_list[key]

def get_srt_files(tr):
    data = ''
    k = tr.video.rfind(".")
    new_srtfile = tr.video[:k] + '.srt'
    if tr.language.name != 'English':
        if os.path.isfile(settings.MEDIA_ROOT + 'videos/' + str(tr.tutorial_detail.foss_id) + '/' + str(tr.tutorial_detail_id) + '/' + new_srtfile.replace(tr.language.name, 'English')):
            data += '<track kind="captions" src="./' + new_srtfile.replace(tr.language.name, 'English') + '" srclang="en" label="English" />'
    if os.path.isfile(settings.MEDIA_ROOT + 'videos/' + str(tr.tutorial_detail.foss_id) + '/' + str(tr.tutorial_detail_id) + '/' + new_srtfile):
        data += '<track kind="captions" src="./' + new_srtfile + '" srclang="en" label="' + tr.language.name + '" />'
    return data

def cd_instruction_sheet(foss, lang):
    file_path = settings.MEDIA_ROOT + 'videos/' + str(foss.id) + '/' + foss.foss.replace(' ', '-') + '-Instruction-Sheet-' + lang.name + '.pdf'
    if lang.name != 'English':
        if os.path.isfile(file_path):
            file_path = '../' + foss.foss.replace(' ', '-') + '-Instruction-Sheet-' + lang.name + '.pdf'
            return file_path


    file_path = settings.MEDIA_ROOT + 'videos/' + str(foss.id) + '/' + foss.foss.replace(' ', '-') + '-Instruction-Sheet-English.pdf'
    if os.path.isfile(file_path):
            file_path = '../' + foss.foss.replace(' ', '-') + '-Instruction-Sheet-English.pdf'
            return file_path
    return False

def cd_installation_sheet(foss, lang):
    file_path = settings.MEDIA_ROOT + 'videos/' + str(foss.id) + '/' + foss.foss.replace(' ', '-') + '-Installation-Sheet-' + lang.name + '.pdf'
    if lang.name != 'English':
        if os.path.isfile(file_path):
            file_path = '../' + foss.foss.replace(' ', '-') + '-Installation-Sheet-' + lang.name + '.pdf'
            return file_path

    file_path = settings.MEDIA_ROOT + 'videos/' + str(foss.id) + '/' + foss.foss.replace(' ', '-') + '-Installation-Sheet-English.pdf'
    if os.path.isfile(file_path):
            file_path = '../' + foss.foss.replace(' ', '-') + '-Installation-Sheet-English.pdf'
            return file_path
    return False

def get_foss_name(foss, key):
    return foss[key]['foss']

def len_cutter(srting, limit):
    return srting[:limit] + (srting[limit:] and '..')

def get_lang_details(foss, key):
    data = ''
    for lang_key, lang_detail in list(foss[key]['langs'].items()):
        data += '<option value="' + str(lang_key) + '">' + lang_detail + '</option>'
    return data
register.filter('get_srt_files', get_srt_files)
register.filter('cd_instruction_sheet', cd_instruction_sheet)
register.filter('cd_installation_sheet', cd_installation_sheet)
register.filter('get_review_status_symbol', get_review_status_symbol)
register.filter('get_review_status_list', get_review_status_list)
register.filter('get_zip_content', get_zip_content)
register.filter('get_foss_name', get_foss_name)
register.filter('len_cutter', len_cutter)
register.filter('get_lang_details', get_lang_details)