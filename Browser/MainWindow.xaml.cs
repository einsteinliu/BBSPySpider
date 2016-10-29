using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.IO;

namespace Browser
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public class Post
    {
        public string File;
        public string Author;
        public string Title;
        public string Time;
        public string Content;
        public string WholePost;
        public string Index;
        public string Url;
    }
    public partial class MainWindow : Window
    {
        string unpublishedFolder = "unpublished\\";
        string publishedRecordFile = "published.dat";
        Dictionary<string, Post> allPosts = new Dictionary<string, Post>();
        Dictionary<string, string> publishedPosts = new Dictionary<string, string>();
        List<string> publishedPostIndex = new List<string>();
        List<string> keys = null;
        List<Post> values = null;
        public MainWindow()
        {
            InitializeComponent();
            loadPublished();
            loadUnpublished();
            loadPosts(0, 20);
        }
        public void loadPublished()
        {
            string[] allPublished = File.ReadAllLines(publishedRecordFile);
            foreach(string line in allPublished)
            {
                string[] paras = line.Split(' ');
                publishedPostIndex.Add(paras[0]);
                publishedPosts[paras[0]] = paras[1];
            }
        }
        public void loadUnpublished()
        {
            string[] allRecords = File.ReadAllLines(unpublishedFolder + "all_posts.dat");
            foreach(string line in allRecords)
            {
                string[] paras = line.Split(' ');
                string filename = unpublishedFolder + paras[1] + ".post";
                allPosts[paras[2]] = parsePostFile(filename);
                allPosts[paras[2]].File = filename;
            }
            keys = allPosts.Keys.ToList();
            values = allPosts.Values.ToList();
        }
        public Post parsePostFile(string file)
        {
            Post post = new Post();
            string[] alllines = File.ReadAllLines(file);
            post.Author = alllines[3];
            post.Index = alllines[0];
            post.Time = alllines[alllines.Length - 1];
            post.Title = alllines[2];
            post.Url = alllines[1];
            post.Content = string.Join("\n", alllines, 2, alllines.Length - 2);
            return post;
        }
        public void loadPosts(int start,int count)
        {
            int currCount = 0;
            int i = start;
            while(currCount<count)
            {
                if (i < allPosts.Count)
                {
                    if (!publishedPostIndex.Contains(allPosts.Keys.ElementAt(i)))
                    {
                        IndexList.Items.Add(allPosts.Keys.ElementAt(i));
                        TitleList.Items.Add(allPosts.Values.ElementAt(i).Title);
                        currCount++;
                    }
                    i++;
                }
                else
                    break;
                
            }
            IndexList.SelectedIndex = 0;
        }

        private void listBox_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            IndexList.SelectedIndex = TitleList.SelectedIndex;                        
        }

        private void IndexList_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            TitleList.SelectedIndex = IndexList.SelectedIndex;
            if(TitleList.SelectedIndex!=-1)
                fillTheForm(IndexList.SelectedItem.ToString());
        }

        public void fillTheForm(string postIndex)
        {
            int index = keys.IndexOf(postIndex);
            Title.Text = values[index].Title;
            ID.Text = values[index].Author;
            Url.Text = values[index].Url;
            PostContent.Text = values[index].Content;
        }

        private void Next_Click(object sender, RoutedEventArgs e)
        {
            string lastIndex = IndexList.Items[IndexList.Items.Count - 1].ToString();
            int start = keys.IndexOf(lastIndex);
            if (start < allPosts.Count)
            {
                IndexList.Items.Clear();
                TitleList.Items.Clear();
                loadPosts(start + 1, 20);
            }
        }

        private void Use_Click(object sender, RoutedEventArgs e)
        {
            Clipboard.SetText(PostContent.Text);
            publishedPostIndex.Add(IndexList.SelectedItem.ToString());
            publishedPosts[IndexList.SelectedItem.ToString()] = allPosts[IndexList.SelectedItem.ToString()].Url;
            int publishedIndex = IndexList.SelectedIndex;
            IndexList.SelectedIndex = -1;
            IndexList.Items.RemoveAt(publishedIndex);
            TitleList.Items.RemoveAt(publishedIndex);
            writePublishedRecord();
        }
        public void writePublishedRecord()
        {
            using (StreamWriter ofs = new StreamWriter("published.dat"))
            {
                for(int i=0;i<publishedPosts.Count;i++)
                {
                    ofs.WriteLine(publishedPosts.Keys.ElementAt(i) + " " + publishedPosts.Values.ElementAt(i));
                }
            }
        }
    }
}
