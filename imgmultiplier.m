%add="C:\\Users\\anstn\\Desktop\\AzureKinectDK\\output_LC3\\outputL\\trans\\%03d.png";
%output="C:\\Users\\anstn\\Desktop\\AzureKinectDK\\output_LC3\\outputL\\trans_times60\\%03d.png";
%"C:\\Users\\anstn\\Desktop\\대학원 2학년\\VCL\\발표자료\\21년 11월 19일 발표자료\\"
output="C:\\Users\\anstn\\Desktop\\AzureKinectDK\\output_LC3\\outputL\\rot90\\trans_times60\\%03d.png";
cadd="C:\\Users\\anstn\\Desktop\\AzureKinectDK\\output_LC3\\outputL\\color\\%03d.png";
tadd="C:\\Users\\anstn\\Desktop\\AzureKinectDK\\output_LC3\\outputL\\trans\\%03d.png";
coutput="C:\\Users\\anstn\\Desktop\\AzureKinectDK\\output_LC3\\outputL\\rot90\\color\\%03d.png";
toutput="C:\\Users\\anstn\\Desktop\\AzureKinectDK\\output_LC3\\outputL\\rot90\\trans\\%03d.png";
for i=1:40
   tgtadd=sprintf(cadd,i);
   a=imread(tgtadd);
   %a = a * 60;
   a= rot90(a);
   imwrite(a, sprintf(coutput,i));
   tgtadd=sprintf(tadd,i);
   a=imread(tgtadd);
   a=rot90(a);
   imwrite(a,sprintf(toutput,i));
   a = a * 60;
   imwrite(a,sprintf(output,i));
end