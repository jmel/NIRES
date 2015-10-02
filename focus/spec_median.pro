pro spec_median

dir = '/Users/jmel/nires/2015-05-26/nsds_krypton_grid/'
file = 'shifts.txt'
templ_file = 'shifts.templ'
outfile = 'shifts_median.txt'

openw, unitw, dir + outfile, /GET_LUN
printf,unitw, 'im_name               x"       y"     dXpix   dYpix  Xpix   Ypix'


restore, '/Users/jmel/nires/2015-04-30/nsds_krypton_grid/'+templ_file
data = read_ascii(dir + file, data_start=1, template=templ)

uniq_im_names = data.im_name[uniq(data.im_name,sort(data.im_name))]

for dx = 1, 8 do begin
   xstart = dx * 256 - 256
   xend = dx * 256
   cx = dx * 256 - 128
   for dy = 1, 4 do begin  
      ystart = dy * 256 - 256 
      yend = dy * 256
      cy = dy * 256 - 128
      for n = 0, n_elements(uniq_im_names) - 1  do begin
         w=where((data.im_name eq uniq_im_names[n]) and $
                 (data.im_x ge xstart) and (data.im_x lt xend) and $
                 (data.field8im_y ge ystart) and (data.field8im_y lt yend), count)
         if (count gt 1) then begin
            xmed = median(data.delta_x[w])
            ymed = median(data.delta_y[w])
            printf, unitw, uniq_im_names[n], data.stage_x[w[0]], data.stage_y[w[0]], $
                    xmed, ymed, cx, cy, format = '(a25, 6(f8.2))'
         endif
      endfor
   endfor
endfor
close, unitw
free_lun, unitw
end

      
