solidity_program=${1}
tool_name='slither'  # Options for the tool name are: manticore, mythril, securify, slither, smartcheck

tools=(slither)
#######################Sanity Check Starts#######################

if [[ -z "${solidity_program}" || ! -f "${solidity_program}" ]]; then
	echo "Solidiy File \"${solidity_program}\" does not exist"
	echo "USAGE: ./run.sh main_contract_file tool_name[${tools[@]}]"
	exit
elif [[ ! " ${tools[@]} " =~ " ${tool_name} " ]]; then
	echo "Please enter correct Tool Name"
	echo "USAGE: ./run.sh main_contract_file tool_name[${tools[@]}]"
	exit
fi

#######################Sanity Check Ends#########################


try_versions_till_bit2 () 
{
	allowed_version=true
	if [[ ${tool_name} == "securify" && ${bit_1} -lt 5 ]]; then # Securify doesn't support versions less than 0.5.0
		bit_1=5
		bit_2=0
	fi

        while [ "$allowed_version" == true ]
        do
		version="${bit_0}.${bit_1}.${bit_2}"
		solc-select install ${version}
                solc_use_result=$(solc-select use ${version})
                allowed_version=false
                echo ${version}
                if [[ ${solc_use_result} == *"Switched global version to"* ]]; then
                        solc $main_contract_file 2> tee -a ${main_contract_file}.txt
                        solc_compile_result=$(cat ${main_contract_file}.txt)
                        rm ${main_contract_file}.txt

			
                        ((bit_2++))
                        allowed_version=true
			return_try_versions_till_bit2=0
                        if [[ $solc_compile_result != *"Error"* ]]; then
				rm ${main_contract_file/.sol/_${tool_name}.txt}
				rm ${main_contract_file/.sol/_${tool_name}.json}
				rm ${main_contract_file/.sol/_${tool_name}_time.txt}
				case $tool_name in
				   "slither")
					slither $main_contract_file 2> tee -a ${main_contract_file}.txt
                        		slither_result=$(cat ${main_contract_file}.txt)
                        		rm ${main_contract_file}.txt
					if [[ $slither_result != *"Error"* ]]; then
                                		allowed_version=false 
						json_output=${main_contract_file/_ext/}
						rm $main_contract_file.json
						rm $main_contract_file.error

						rm $json_output.json
						rm $json_output.error

						{ time slither --json $json_output.json  $main_contract_file; } 2> ${main_contract_file/.sol/_${tool_name}_time.txt}
						#echo "YES YES YES"
						return_try_versions_till_bit2=1

					fi
					;;
				   esac
				
			
                        fi

                        echo $version
                fi
        done
}

no_version ()
{
	version=0.1.2
	bit_0=0
	bit_1=1
	bit_2=2
	try_versions_till_bit2
	for bit_1 in {2..8}
	do
		bit_2=0
		if [[ return_try_versions_till_bit2 -eq 0 ]]; then
			try_versions_till_bit2
		fi
	done
}

version_gte_lt ()
{
	echo $version
	version=$(echo $version | grep -o '[[:digit:]]*')
	arrIN=(${version//./ })
	for i in {0..5}
	do
		eval "bit_${i}=${arrIN[i]}";
	done
	start_version="${bit_0}.${bit_1}.${bit_2}"
	end_version="${bit_3}.${bit_4}.${bit_5}"

	version=${start_version}
	try_versions_till_bit2
	if [[ ${bit_1} -lt ${bit_4} && return_try_versions_till_bit2 -eq 0 ]]; then
		bit_2=0
		((bit_1++))
		try_versions_till_bit2
	fi
}

complex_version ()
{
	if [[ $version == *">"* &&  $version == *"<"* ]]; then
		version_gte_lt
	else
		simple_version
	fi
}
simple_version ()
{
	echo "Simple_Version"
	echo ${version}
	version=$(echo $version | tr -d "^")
	version=$(echo $version | tr -d ">")
	version=$(echo $version | tr -d "<")
	version=$(echo $version | tr -d "=")
	version=$(echo $version | grep -o '[[:digit:]]*')
        echo "VERSION: "${version}
	version=$(echo $version | sed  's/ /./g')

        echo "VERSION 2: "${version}
	arrIN=(${version//./ })
	
	

        for i in {0..2}
        do      
                eval "bit_${i}=${arrIN[i]}";
        done
	try_versions_till_bit2
}

check_is_folder ()
{
	is_folder=0
	if [[ $(grep '\"content\":' ${solidity_program}) ]]; then
		is_folder=1
	fi
	if [[ ${is_folder} -eq 0 ]]; then
		main_contract_file=$solidity_program
	elif [[ ${is_folder} -eq 1 ]]; then
		main_contract_name=$(grep ${solidity_program} contract_name.txt  | awk '{print $2}')
		cd ${solidity_program/.sol/}
		main_contract_file=$(find . -iname "${main_contract_name}.sol" | sed 's/.\///g')
	fi
}

check_is_folder

	return_try_versions_till_bit2=0
	version=$(cat $main_contract_file | grep pragma  |  sed 's/;.*//' | tr -d ";")


	pragma=pragma
	s=${version//"$pragma"}
	count_pragma=$(echo "$(((${#version} - ${#s}) / ${#pragma}))")

	if [[ $count_pragma == 1 ]]; then
		
		if [[ $version == *"^"* ]]; then
			simple_version
		elif [[ $version == *">"* ||  $version == *">"* ]]; then
			complex_version
		fi

	elif [[ $count_pragma == 0 ]]; then
		no_version
	fi
