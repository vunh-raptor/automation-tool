#html template for external maitenance email
external_maintenance_notification_html = """<img src = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRExyT1HEwoJgvU1fV0i6TO9ErQGERC8DwBnw&s"> <p>Kính gửi quý đối tác</p>
<p>Công ty Home Credit có kế hoạch bảo trì hệ thống định kì. Các dịch vụ đang cung cấp cho quý khách có thể bị gián đoạn trong khoảng thời gian sau đây.</p>
<ul><li>Bắt đầu: {start}</li>
<li>Kết thúc: {end} </li></ul>
<p>Kính mong Quý đối tác thông cảm và lưu ý bỏ qua các thông tin cảnh báo (nếu có) từ hệ thống.</p>
<p>Trân trọng cám ơn.</p>
<p>HCVN IT</p>
<hr>
<p>Dear valued partner</p>
<p>Home Credit Vietnam is going to do IT system maaintenance. The services that are providing to you will be impacted during below duration:</p>
<ul><li>Start: {start_eng}</li>
<li>End: {end_eng} </li></ul>
<p>Please kindly ignore the alert (if any) from your mornitoring system for those services.</p>
<p>Best Regards,</p>
<p>HCVN IT</p>"""

#html template for internal maitenance email
internal_maintenance_notification_html = """<img src = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRExyT1HEwoJgvU1fV0i6TO9ErQGERC8DwBnw&s"><p>Dear all,</p>
<p>We would like to inform you about following maintenance:</p>
<p><b>Description:</b> {description}</p>
<p><b>Start time: </b>{start}</p>
<p><b>End time: </b> {end}</p>
<p><b>Impacted Services:</b>{impactedService}</p>
<p>Do not hestitate to call us via 'HCVN IT Hotline' in MS Team for help in case of any questions</p>
<p>HCVN IT</p>"""

#html template for incident notification email
incident_notification_template_html = """<div style="width: 100%; margin-left: auto; margin-right: auto;">
<div style="text-align: center;"><img src = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRExyT1HEwoJgvU1fV0i6TO9ErQGERC8DwBnw&s"></div>
<p></p>
<p style="text-align: center; color:blue; width:50%; margin-left: auto; margin-right: auto;"><b>Incident Ticket Number:    </b><span style="color:black; margin-left: 50px">{ticketNumber}</span></p>
<p style="text-align: center; color:blue;"><b>Description:   </b><span style="color:black; margin-left: 20px">{description}</span></p>
<p style="text-align: center; color:blue;"><b>Business Impact:   </b><span style="color:black; margin-left: 20px">{businessImpact}</span></p>
<hr color="blue" noshade width="50%" align="center">
<p style="text-align: center; color:blue;"><b>Current Status:   </b><span style="color:black; margin-left: 20px">{currentStatus}</p>
<p></p>
<p>Do not hestitate to call us via 'HCVN IT Hotline' for help in any questions</p>
</div>"""