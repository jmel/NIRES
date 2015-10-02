pro focus_spec

dir = '/Users/jmel/nires/2015-05-26/nsds_krypton_grid/'
kdir = '/Users/jmel/nires/krypton_grid/'
region_file = 'centroid.reg'
openr, unitr, kdir + region_file, /GET_LUN

outfile = 'shifts.txt'
openw, unitw, dir + outfile, /GET_LUN

outreg_file = 'centreg.reg'
openw, unitreg, dir + outreg_file, /GET_LUN 
printf, unitreg, 'global color=green dashlist=8 3 width=1 font="helvetica 10 normal" select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1'
printf, unitreg, 'physical'

data_file = 'README'
template_file = 'data.templ'
restore, kdir + template_file
data = read_ascii(dir + data_file, data_start=1, template=templ)

sz = size(data.field1)
n_im = sz[1]
im_array = fltarr(2048, 1024, n_im)
for i = 0, n_im - 1 do begin
   im_array[*, *, i] = readfits(dir + data.field1[i]) - readfits(dir + data.field2[i])
endfor 

s1 = ''
bsize = 5
xshift = -3
yshift = 0
;atv,fltarr(bsize * 2, bsize * 2)
;atv_zoom, 'in'
;atv_zoom, 'in'

while not EOF(unitr) do begin
   readf, unitr, s1
   if strpos(s1, 'circle') NE -1 then begin
      s1 = strrep(strrep(s1, 'circle(', ''), ')', '')
      pos_array = strsplit(s1, ',', /EXTRACT)
      x=2048 - pos_array[1]
      y=1024 - pos_array[0]
      refx = 0
      refy = 0
      for i = 0, n_im - 1 do begin
         sub_im = im_array[x - bsize - xshift: x + bsize - xshift, $
                           y - bsize - yshift: y + bsize - yshift, i]
         XCEN = -1
         YCEN = -1
         gcntrd, sub_im, bsize, bsize, XCEN, YCEN, 1.5, /SILENT
         print, XCEN, YCEN
         if (XCEN GT 0) and (YCEN GT 0) and (XCEN LT (bsize * 2)) and (YCEN LT (bsize * 2)) then begin
            centx = XCEN - bsize 
            centy = YCEN - bsize
            print, centx, centy
            if i EQ 0 then begin
               refx = centx
               refy = centy
            endif
            if (refx NE 0) then begin
               print, data.field1[i], data.field2[i], data.field3[i], data.field4[i], centx - refx , centy - refy, $
                 pos_array[0] + centx - xshift + 0.5, pos_array[1] + centy - yshift + 0.5, format='(a25, a25, 6(f8.2))'
               printf, unitw, data.field1[i], data.field2[i], data.field3[i], data.field4[i], centx - refx, centy - refy, $
                 x + centx - xshift + 0.5, y + centy - yshift + 0.5, format='(a25, a25, 6(f8.2))'
               if i EQ 0 then begin
                  printf, unitreg, x + centx - xshift, y + centy - yshift, 2, format='("circle(",f8.2,",",f8.2,",",f5.1,")")'
               endif

;               atv, sub_im
;               atvplot, XCEN, YCEN, psym=4
;               g=get_kbrd(1)
            endif
         endif else begin
             print, data.field1[i], data.field2[i], data.field3[i], data.field4[i], 'Bad Centroid' , XCEN, YCEN, $
                    format='(2a25,2f8.1,a15,2f8.1)'
          endelse
      endfor
   endif
endwhile
close, unitr
free_lun, unitr
close, unitw
free_lun, unitw
close, unitreg
free_lun, unitreg
end

      
